"""Load the character and reusable content library.

The loader is deliberately small for the first migration step.  It provides a
stable interface for the CLI while the existing curated pools are moved into
JSON-backed data files.
"""

from dataclasses import dataclass
import json
from pathlib import Path

DATA_ROOT = Path(__file__).parent / "data"


@dataclass(frozen=True)
class CharacterLibrary:
    """Content needed by the current scene composer."""

    character_id: str
    themes: dict[str, dict[str, list[str]]]
    global_pools: dict[str, list[str]]


@dataclass(frozen=True)
class ContentPack:
    """Reusable content independent of any one character."""

    pack_id: str
    name: str
    entries: dict[str, list[str]]


def list_characters() -> list[str]:
    """Return available character IDs in stable filename order."""
    return sorted(path.stem for path in (DATA_ROOT / "characters").glob("*.json"))


def list_packs() -> list[str]:
    """Return available reusable pack IDs in stable filename order."""
    return sorted(path.stem for path in (DATA_ROOT / "packs").glob("*.json"))


def list_themes(character_id: str) -> list[str]:
    """Return the available theme names for one character."""
    return list(load_character(character_id).themes)


def load_character(character_id: str = "miyuki") -> CharacterLibrary:
    """Return a character library using the current curated content.

    The runtime source is JSON under ``data/``. Legacy Python pools are used
    only by the explicit migration utility.
    """
    character_path = DATA_ROOT / "characters" / f"{character_id}.json"
    if not character_path.exists():
        raise ValueError(f"Unknown character: {character_id}")
    character = json.loads(character_path.read_text(encoding="utf-8"))
    loaded_themes = character.get("themes")
    global_path = DATA_ROOT / "global" / "pools.json"
    loaded_global_pools = json.loads(global_path.read_text(encoding="utf-8"))
    _validate_themes(loaded_themes)
    _validate_pools(loaded_global_pools, "global pools")

    return CharacterLibrary(
        character_id=character_id,
        themes=loaded_themes,
        global_pools=loaded_global_pools,
    )


def load_pack(pack_id: str) -> ContentPack:
    """Load one reusable content pack from ``data/packs``."""
    path = DATA_ROOT / "packs" / f"{pack_id}.json"
    if not path.exists():
        raise ValueError(f"Unknown pack: {pack_id}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    entries = payload.get("entries")
    _validate_pools(entries, f"pack {pack_id!r}")
    if payload.get("id") != pack_id or not isinstance(payload.get("name"), str):
        raise ValueError(f"pack {pack_id!r} has invalid metadata")
    return ContentPack(pack_id=pack_id, name=payload["name"], entries=entries)


def _validate_pools(value: object, label: str) -> None:
    if not isinstance(value, dict) or not value:
        raise ValueError(f"{label} must be a non-empty object")
    if any(not isinstance(key, str) or not isinstance(options, list) or not options
           or any(not isinstance(option, str) and not isinstance(option, dict) for option in options)
           or any(isinstance(option, str) and not option.strip() for option in options)
           or any(isinstance(option, dict) and (not isinstance(option.get("text"), str) or not option["text"].strip()) for option in options)
           or any(isinstance(option, dict) and any(
               key in option and (not isinstance(option[key], list) or not all(isinstance(tag, str) for tag in option[key]))
               for key in ("tags", "requires", "exclude")
           ) for option in options)
           for key, options in value.items()):
        raise ValueError(f"{label} must map names to non-empty string lists")


def _validate_themes(value: object) -> None:
    if not isinstance(value, dict) or not value:
        raise ValueError("themes must be a non-empty object")
    for theme_name, blocks in value.items():
        if not isinstance(theme_name, str) or not isinstance(blocks, dict):
            raise ValueError("themes must map names to block objects")
        _validate_pools(blocks, f"theme {theme_name!r}")
