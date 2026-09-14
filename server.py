from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# --- IMPORT YOUR POOLS ---
# (Assume pools is imported from your pools.py)
from data_loader import list_characters, list_packs, list_themes, load_character, load_pack
from engine import SceneRequest, resolve_scene, scene_request_from_payload
from history import list_scenes, save_scene, set_favourite
from prompt_compiler import SYSTEM_PROMPT, compile_prompt_request

app = FastAPI()

# This allows your website to talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
HISTORY_DB = os.environ.get("HISTORY_DB", "history.sqlite3")


@app.get("/characters")
async def characters():
    return {"characters": list_characters()}


@app.get("/packs")
async def packs():
    return {"packs": list_packs()}


@app.get("/characters/{character_id}/themes")
async def themes(character_id: str):
    return {"character_id": character_id, "themes": list_themes(character_id)}


@app.get("/history")
async def history(limit: int = 50):
    return {"scenes": list_scenes(HISTORY_DB, limit)}


@app.post("/history")
async def save_history(payload: dict):
    request = scene_request_from_payload(payload)
    library = load_character(request.character_id)
    selected_packs = [load_pack(pack_id) for pack_id in request.pack_ids]
    theme_name, seeds = resolve_scene(library, request, packs=selected_packs)
    scene_id = save_scene(HISTORY_DB, request.character_id, theme_name, dict(payload), seeds, request.seed)
    return {"id": scene_id, "character_id": request.character_id, "theme": theme_name, "seeds": seeds}


@app.patch("/history/{scene_id}/favourite")
async def favourite(scene_id: int, enabled: bool = True):
    return {"updated": set_favourite(HISTORY_DB, scene_id, enabled)}


@app.post("/scene/randomize")
async def randomize_scene(character_id: str = "miyuki", theme_name: str | None = None, pack_ids: str = "", seed: int | None = None):
    library = load_character(character_id)
    selected_packs = [load_pack(pack_id.strip()) for pack_id in pack_ids.split(",") if pack_id.strip()]
    theme_name, seeds = resolve_scene(
        library,
        SceneRequest(character_id=character_id, theme_name=theme_name, pack_ids=tuple(pack_ids.split(",")), seed=seed),
        packs=selected_packs,
    )
    return {"character_id": character_id, "theme": theme_name, "seeds": seeds}


@app.post("/scene/resolve")
async def resolve_scene_request(payload: dict):
    request = scene_request_from_payload(payload)
    library = load_character(request.character_id)
    selected_packs = [load_pack(pack_id) for pack_id in request.pack_ids]
    theme_name, seeds = resolve_scene(library, request, packs=selected_packs)
    return {"character_id": request.character_id, "theme": theme_name, "seeds": seeds}

@app.get("/generate-prompt")
async def generate_ai_prompt(character_id: str = "miyuki", theme_name: str | None = None, pack_ids: str = "", seed: int | None = None):
    library = load_character(character_id)
    packs = [load_pack(pack_id.strip()) for pack_id in pack_ids.split(",") if pack_id.strip()]
    theme_name, seeds = resolve_scene(
        library,
        SceneRequest(character_id=character_id, theme_name=theme_name, pack_ids=tuple(pack_ids.split(",")), seed=seed),
        packs=packs,
    )
    user_request = compile_prompt_request(seeds)
    
    # 3. Call Gemini
    if not GEMINI_API_KEY:
        raise RuntimeError("Set GEMINI_API_KEY in the environment before generating a prompt.")
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_request,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.3),
    )
    
    # 4. Return the seeds + the expansion back to the website
    return {
        "character_id": character_id,
        "theme": theme_name,
        "seeds": seeds,
        "expanded_prompt": response.text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
