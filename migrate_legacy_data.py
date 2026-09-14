"""One-time migration of the curated legacy pools into JSON.

Run from the project directory with:

    python migrate_legacy_data.py

The script is intentionally kept in the repository so the migration is
auditable and repeatable. It does not alter the legacy Python source.
"""

import json
from pathlib import Path

import pools


ROOT = Path(__file__).parent


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    write_json(ROOT / "data" / "global" / "pools.json", pools.global_pools)
    character = {
        "id": "miyuki",
        "name": "Miyuki",
        "identity": {
            "core": pools.LOCKED_CORE_IDENTITY,
            "hair_base": pools.LOCKED_HAIR_BASE,
        },
        "themes": pools.themes,
    }
    write_json(ROOT / "data" / "characters" / "miyuki.json", character)
    print("Migrated global pools and Miyuki themes to data/.")


if __name__ == "__main__":
    main()
