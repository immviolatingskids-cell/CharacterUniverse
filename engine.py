"""Character-agnostic scene selection and seed-matrix construction."""

import random
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field

from data_loader import CharacterLibrary, ContentPack


Entry = str | Mapping[str, object]


@dataclass(frozen=True)
class SceneRequest:
    character_id: str = "miyuki"
    theme_name: str | None = None
    pack_ids: tuple[str, ...] = ()
    context_tags: frozenset[str] = frozenset()
    overrides: Mapping[str, str] = field(default_factory=dict)
    seed: int | None = None


def scene_request_from_payload(payload: Mapping[str, object]) -> SceneRequest:
    """Parse a JSON-compatible request payload into the core request model."""
    if not isinstance(payload, Mapping):
        raise ValueError("Scene request must be an object")
    character_id = payload.get("character_id", "miyuki")
    theme_name = payload.get("theme_name")
    pack_ids = payload.get("pack_ids", ())
    context_tags = payload.get("context_tags", ())
    overrides = payload.get("overrides", {})
    seed = payload.get("seed")
    if not isinstance(character_id, str) or (theme_name is not None and not isinstance(theme_name, str)):
        raise ValueError("character_id and theme_name must be strings")
    if not isinstance(pack_ids, (list, tuple)) or not all(isinstance(item, str) for item in pack_ids):
        raise ValueError("pack_ids must be a list of strings")
    if not isinstance(context_tags, (list, tuple, set, frozenset)) or not all(isinstance(item, str) for item in context_tags):
        raise ValueError("context_tags must be a list of strings")
    if not isinstance(overrides, Mapping) or not all(isinstance(key, str) and isinstance(value, str) for key, value in overrides.items()):
        raise ValueError("overrides must map block names to strings")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise ValueError("seed must be an integer")
    return SceneRequest(
        character_id=character_id,
        theme_name=theme_name,
        pack_ids=tuple(pack_ids),
        context_tags=frozenset(context_tags),
        overrides=dict(overrides),
        seed=seed,
    )


def entry_text(entry: Entry) -> str:
    return entry if isinstance(entry, str) else str(entry["text"])


def compatible(entry: Entry, context_tags: set[str]) -> bool:
    """Return whether an entry is allowed in a tagged scene context.

    Legacy string entries remain compatible everywhere. Structured entries can
    opt into ``requires`` and ``exclude`` without involving an AI service.
    """
    if isinstance(entry, str):
        return True
    required = set(entry.get("requires", []))
    excluded = set(entry.get("exclude", []))
    return required.issubset(context_tags) and not excluded.intersection(context_tags)


def compatible_options(options: Sequence[Entry], context_tags: set[str]) -> list[Entry]:
    """Filter options and reject a pool with no compatible candidates."""
    return [entry for entry in options if compatible(entry, context_tags)]


def merge_packs(
    theme: Mapping[str, Sequence[Entry]],
    packs: Sequence[ContentPack] = (),
) -> dict[str, list[Entry]]:
    """Return a scene pool with reusable pack entries appended by block."""
    merged = {key: list(options) for key, options in theme.items()}
    for pack in packs:
        for key, options in pack.entries.items():
            merged.setdefault(key, []).extend(options)
    return merged


def resolve_scene(
    library: CharacterLibrary,
    request: SceneRequest,
    packs: Sequence[ContentPack] = (),
    rng: random.Random | None = None,
) -> tuple[str, dict[str, str]]:
    """Resolve a structured scene request into its theme name and seeds."""
    if request.character_id != library.character_id:
        raise ValueError("Request character does not match the loaded library")
    theme_name = request.theme_name or next(iter(library.themes))
    if theme_name not in library.themes:
        raise ValueError(f"Unknown theme: {theme_name}")
    theme = merge_packs(library.themes[theme_name], packs)
    if request.seed is not None:
        rng = random.Random(request.seed)
    return theme_name, build_seed_matrix(
        library,
        theme,
        context_tags=set(request.context_tags),
        overrides=request.overrides,
        rng=rng,
    )


def choose_random(options: Sequence[Entry], rng: random.Random | None = None) -> Entry:
    """Choose one content entry, with a useful error for malformed input."""
    if not options:
        raise ValueError("Cannot choose from an empty pool")
    return (rng or random).choice(options)


def build_seed_matrix(
    library: CharacterLibrary,
    theme: Mapping[str, Sequence[str]],
    choose: Callable[[str, Sequence[Entry]], Entry] | None = None,
    rng: random.Random | None = None,
    context_tags: set[str] | None = None,
    packs: Sequence[ContentPack] = (),
    overrides: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Resolve a theme and global pools into one structured seed matrix.

    ``choose`` is injected by the CLI for interactive choices and by tests or
    future APIs for explicit selections. Without it, all blocks are random.
    """
    chooser = choose or (lambda _key, options: choose_random(options, rng))
    tags = context_tags or set()
    pools = merge_packs(theme, packs)
    pools = {key: compatible_options(options, tags) for key, options in pools.items()}
    empty_pools = [key for key, options in pools.items() if not options]
    if empty_pools:
        raise ValueError(f"No compatible entries for block(s): {', '.join(empty_pools)}")
    pools.update({key: compatible_options(options, tags) for key, options in library.global_pools.items()})
    overrides = overrides or {}
    resolved = {}
    for key, options in pools.items():
        if key in overrides:
            selected = overrides[key]
            if selected not in {entry_text(option) for option in options}:
                raise ValueError(f"Override for {key!r} is not available in the selected pool")
            resolved[key] = selected
        else:
            resolved[key] = entry_text(chooser(key, options))
    return resolved
