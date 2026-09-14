import json
import unittest
import tempfile
from pathlib import Path

from data_loader import list_characters, list_packs, list_themes, load_character, load_pack
from engine import SceneRequest, build_seed_matrix, compatible, compatible_options, merge_packs, resolve_scene, scene_request_from_payload
from prompt_compiler import compile_prompt_request
from history import list_scenes, save_scene, set_favourite


class DataLoaderTests(unittest.TestCase):
    def test_miyuki_is_loaded_from_json(self):
        library = load_character("miyuki")
        character_file = Path(__file__).parents[1] / "data" / "characters" / "miyuki.json"
        payload = json.loads(character_file.read_text(encoding="utf-8"))

        self.assertEqual(library.character_id, "miyuki")
        self.assertEqual(library.themes, payload["themes"])
        self.assertEqual(len(library.themes), 6)
        self.assertEqual(len(library.global_pools), 9)

    def test_unknown_character_fails_clearly(self):
        with self.assertRaises(ValueError):
            load_character("does-not-exist")

    def test_library_listing_is_filename_based_and_stable(self):
        self.assertEqual(list_characters(), ["miyuki", "ren"])
        self.assertEqual(list_packs(), ["streetwear"])
        self.assertEqual(list_themes("ren"), ["1. Neon Courier"])

    def test_reusable_pack_is_loaded_independently(self):
        pack = load_pack("streetwear")
        self.assertEqual(pack.pack_id, "streetwear")
        self.assertIn("WARDROBE", pack.entries)
        self.assertEqual(pack.entries["WARDROBE"][0]["text"], "oversized charcoal hoodie with clean structural lines")

    def test_pack_rejects_malformed_compatibility_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pack_dir = root / "packs"
            pack_dir.mkdir()
            (pack_dir / "bad.json").write_text(
                '{"id":"bad","name":"Bad","entries":{"WARDROBE":[{"text":"coat","exclude":"winter"}]}}',
                encoding="utf-8",
            )
            import data_loader
            original_root = data_loader.DATA_ROOT
            data_loader.DATA_ROOT = root
            try:
                with self.assertRaises(ValueError):
                    load_pack("bad")
            finally:
                data_loader.DATA_ROOT = original_root

    def test_pack_entries_merge_without_mutating_character_theme(self):
        library = load_character("miyuki")
        pack = load_pack("streetwear")
        original = list(next(iter(library.themes.values()))["WARDROBE"])
        merged = merge_packs(next(iter(library.themes.values())), [pack])
        self.assertEqual(next(iter(library.themes.values()))["WARDROBE"], original)
        self.assertEqual(len(merged["WARDROBE"]), len(original) + len(pack.entries["WARDROBE"]))
        self.assertIn("ACCESSORIES", merged)

    def test_second_character_uses_the_same_loader(self):
        library = load_character("ren")
        self.assertEqual(library.character_id, "ren")
        self.assertIn("1. Neon Courier", library.themes)
        self.assertEqual(len(library.global_pools), 9)

    def test_engine_resolves_any_character_theme_without_hardcoded_blocks(self):
        library = load_character("ren")
        theme = next(iter(library.themes.values()))
        seeds = build_seed_matrix(library, theme, choose=lambda _key, options: options[0])
        self.assertEqual(seeds["CASTING"], theme["CASTING"][0])
        self.assertEqual(seeds["ACTION"], theme["ACTION"][0])
        self.assertEqual(seeds["CAMERA_DEVICE"], library.global_pools["CAMERA_DEVICE"][0])

    def test_engine_accepts_valid_block_overrides(self):
        library = load_character("ren")
        theme = next(iter(library.themes.values()))
        selected = theme["WARDROBE"][0]
        seeds = build_seed_matrix(library, theme, overrides={"WARDROBE": selected})
        self.assertEqual(seeds["WARDROBE"], selected)
        with self.assertRaises(ValueError):
            build_seed_matrix(library, theme, overrides={"WARDROBE": "not in the pool"})

    def test_structured_scene_request_resolves_named_theme(self):
        library = load_character("ren")
        theme_name, seeds = resolve_scene(
            library,
            SceneRequest(character_id="ren", theme_name="1. Neon Courier"),
        )
        self.assertEqual(theme_name, "1. Neon Courier")
        self.assertIn("WARDROBE", seeds)

    def test_scene_seed_reproduces_the_same_matrix(self):
        library = load_character("miyuki")
        request = SceneRequest(character_id="miyuki", seed=42)
        first = resolve_scene(library, request)[1]
        second = resolve_scene(library, request)[1]
        self.assertEqual(first, second)

    def test_unknown_theme_fails_clearly(self):
        library = load_character("ren")
        with self.assertRaises(ValueError):
            resolve_scene(library, SceneRequest(character_id="ren", theme_name="missing"))

    def test_scene_history_round_trips_locally(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "history.sqlite3"
            scene_id = save_scene(database, "ren", "1. Neon Courier", {"seed": 4}, {"ACTION": "deliver"}, 4)
            scenes = list_scenes(database)
            self.assertEqual(scenes[0]["id"], scene_id)
            self.assertEqual(scenes[0]["seeds"]["ACTION"], "deliver")
            self.assertTrue(set_favourite(database, scene_id))
            self.assertEqual(list_scenes(database)[0]["favourite"], 1)
            self.assertFalse(set_favourite(database, 999))

    def test_scene_payload_parser_validates_and_normalizes_json(self):
        request = scene_request_from_payload({
            "character_id": "ren",
            "pack_ids": ["streetwear"],
            "context_tags": ["night"],
            "overrides": {"ACTION": "deliver a parcel"},
            "seed": 7,
        })
        self.assertEqual(request.pack_ids, ("streetwear",))
        self.assertEqual(request.context_tags, frozenset({"night"}))
        self.assertEqual(request.seed, 7)
        with self.assertRaises(ValueError):
            scene_request_from_payload({"seed": True})

    def test_prompt_compiler_preserves_resolved_values(self):
        request = compile_prompt_request({"CASTING": "TEST SUBJECT", "ACTION": "TEST ACTION", "HOBBY": "TEST HOBBY"})
        self.assertIn("TEST SUBJECT", request)
        self.assertIn("TEST ACTION", request)
        self.assertIn("[HOBBY]: TEST HOBBY", request)

    def test_compatibility_metadata_is_deterministic_and_optional(self):
        self.assertTrue(compatible("legacy entry", {"winter"}))
        self.assertTrue(compatible({"text": "coat", "requires": ["winter"]}, {"winter"}))
        self.assertFalse(compatible({"text": "coat", "requires": ["winter"]}, {"summer"}))
        self.assertFalse(compatible({"text": "coat", "exclude": ["tropical"]}, {"tropical"}))
        options = compatible_options(
            [{"text": "coat", "requires": ["winter"]}, {"text": "shirt", "exclude": ["winter"]}],
            {"winter"},
        )
        self.assertEqual(options[0]["text"], "coat")
        self.assertEqual(compatible_options([{"text": "coat", "exclude": ["winter"]}], {"winter"}), [])


if __name__ == "__main__":
    unittest.main()
