# CharacterUniverse

A small local tool for composing character and image-generation prompts.

## Architecture

```text
data/ → data_loader.py → engine.py → prompt_compiler.py → Gemini (optional)
                              ↑
                         CLI / FastAPI
```

Characters, global pools, and reusable packs are JSON-backed. The engine handles
selection, deterministic seeds, pack merging, compatibility tags, and explicit
block overrides without depending on Gemini or FastAPI.

## Layout

- `data/characters/` — character identity and themes
- `data/global/` — reusable technical pools
- `data/packs/` — reusable content packs
- `tests/` — standard-library unit tests
- `pools.py` — legacy migration source; runtime code does not import it

## Verify

```text
python -m unittest discover -s tests -v
```

## CLI

Set `GEMINI_API_KEY` in the environment, then run:

```text
python img.py
```

The Python entry point also accepts `character_id`, `pack_ids`, and `seed` when
called programmatically.

## API

Install dependencies from `requirements.txt`, set `GEMINI_API_KEY`, and run:

```text
uvicorn server:app --reload
```

Useful endpoints include `/characters`, `/packs`, `/scene/randomize`,
`/scene/resolve`, `/history`, and `/generate-prompt`.
