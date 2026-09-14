# img.py
import os
import random
from pathlib import Path
from engine import build_seed_matrix, merge_packs
from prompt_compiler import SYSTEM_PROMPT, compile_prompt_request

try:
    from data_loader import load_character, load_pack
except ImportError:
    print("❌ Error: Could not load the content library.")
    exit(1)

try:
    from config import GEMINI_API_KEY
except ImportError:
    print("❌ Error: Could not find 'config.py'.")
    exit(1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_theme(themes, character_name):
    clear_screen()
    print(f"=== SELECT {character_name.upper()}'S SCENARIO ===")
    theme_names = list(themes.keys())
    for idx, name in enumerate(theme_names, 1):
        print(f"{idx}. {name}")
    print("=" * 40)
    
    while True:
        choice = input(f"Select a scenario (1-{len(theme_names)}): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(theme_names):
                selected_key = theme_names[idx - 1]
                return themes[selected_key]
        print("❌ Invalid choice.")

def interactive_choice(block_name, options):
    if len(options) == 1:
        return options[0]

    clear_screen()
    print(f"=== SELECT FOR: {block_name.upper()} ===")
    print("0. 🎲 [RANDOMIZE THIS BLOCK]")
    for idx, opt in enumerate(options, 1):
        preview = opt if len(opt) <= 70 else f"{opt[:70]}..."
        print(f"{idx}. {preview}")
    print("=" * 40)
    
    while True:
        choice = input(f"Choose option (0-{len(options)}) [Default: Random]: ").strip()
        if choice == "" or choice == "0":
            return random.choice(options)
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("❌ Invalid choice.")

def generate_ai_prompt(character_id="miyuki", pack_ids=(), seed=None):
    library = load_character(character_id)
    packs = [load_pack(pack_id) for pack_id in pack_ids]
    themes = {name: merge_packs(theme, packs) for name, theme in library.themes.items()}
    active_pool = select_theme(themes, character_id)
    seeds = build_seed_matrix(
        library,
        active_pool,
        choose=interactive_choice,
        rng=random.Random(seed) if seed is not None else None,
    )

    clear_screen()
    print("✅ Curated Matrix compiled successfully!")
    print("-" * 60)
    
    user_request = compile_prompt_request(seeds)

    print("\n✨ Forwarding director specifications to Gemini...")
    try:
        if not GEMINI_API_KEY:
            raise RuntimeError("Set GEMINI_API_KEY in the environment before generating a prompt.")
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_request,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.3)
        )
    except Exception as e:
        print(f"❌ Gemini API error: {e}"); exit(1)

    return response.text

if __name__ == "__main__":
    ai_prompt = generate_ai_prompt()
    Path("prompt.txt").write_text(ai_prompt, encoding="utf-8")
    print("\n🎉 Master Director Prompt saved to 'prompt.txt'\n")
    print(ai_prompt)
