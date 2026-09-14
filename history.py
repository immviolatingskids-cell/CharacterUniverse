"""Local SQLite persistence for resolved scene compositions."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def initialize(database: str | Path) -> None:
    connection = sqlite3.connect(database)
    try:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS scenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id TEXT NOT NULL,
                theme_name TEXT NOT NULL,
                seed INTEGER,
                request_json TEXT NOT NULL,
                seeds_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                favourite INTEGER NOT NULL DEFAULT 0
            )"""
        )
        connection.commit()
    finally:
        connection.close()


def save_scene(database: str | Path, character_id: str, theme_name: str,
               request: dict[str, Any], seeds: dict[str, str], seed: int | None = None) -> int:
    initialize(database)
    connection = sqlite3.connect(database)
    try:
        cursor = connection.execute(
            """INSERT INTO scenes
            (character_id, theme_name, seed, request_json, seeds_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (character_id, theme_name, seed, json.dumps(request, sort_keys=True),
             json.dumps(seeds, ensure_ascii=False, sort_keys=True),
             datetime.now(timezone.utc).isoformat()),
        )
        scene_id = int(cursor.lastrowid)
        cursor.close()
        connection.commit()
        return scene_id
    finally:
        connection.close()


def list_scenes(database: str | Path, limit: int = 50) -> list[dict[str, Any]]:
    if limit < 1:
        raise ValueError("limit must be positive")
    initialize(database)
    connection = sqlite3.connect(database)
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(
            "SELECT * FROM scenes ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        cursor.close()
    finally:
        connection.close()
    return [
        {**dict(row), "request": json.loads(row["request_json"]), "seeds": json.loads(row["seeds_json"])}
        for row in rows
    ]


def set_favourite(database: str | Path, scene_id: int, favourite: bool = True) -> bool:
    """Set a scene's favourite flag and return whether it existed."""
    initialize(database)
    connection = sqlite3.connect(database)
    try:
        cursor = connection.execute(
            "UPDATE scenes SET favourite = ? WHERE id = ?",
            (int(favourite), scene_id),
        )
        changed = cursor.rowcount > 0
        cursor.close()
        connection.commit()
        return changed
    finally:
        connection.close()
