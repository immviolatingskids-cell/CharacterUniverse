"""Compile a resolved seed matrix into the Gemini request text."""


SYSTEM_PROMPT = (
    "You are an expert film director and photorealistic AI prompt engineer. "
    "Your task is to take micro-level character specs, camera intent, and lighting dynamics "
    "and synthesize them into a descriptive master prompt using a clean markdown layout. "
    "Never alter the core subject identity or facial traits provided."
)


def compile_prompt_request(seeds: dict[str, str]) -> str:
    """Build the stable prompt request from a resolved seed matrix."""
    get = seeds.get
    known = {
        "CASTING", "HAIR_STYLING", "WARDROBE", "MICRO_EXPRESSION", "ACTION",
        "PROPS", "LOCATION", "CAPTURE_INTENT", "CAMERA_DEVICE", "LENS_SPECS",
        "COMPOSITION_FRAMING", "TIME_OF_DAY", "WEATHER", "LIGHTING_BEHAVIOR",
        "COLOUR_SIMULATION",
    }
    additional = "\n".join(
        f"    [{key}]: {value}" for key, value in seeds.items() if key not in known
    )
    additional_section = (
        f"\n    --- ADDITIONAL SCENE BLOCKS ---\n{additional}\n"
        if additional else ""
    )
    return f"""
    Expand the following curated seed matrix into a detailed, ultra-realistic image generation prompt in markdown (### Scene, ### Subject, ### Environment, ### Lighting, ### Camera, ### Negative Prompts).

    --- CURATED SEED MATRIX ---
    [SUBJECT CORE]: {get('CASTING')}
    [HAIR & STYLING]: {get('HAIR_STYLING')}
    [WARDROBE]: {get('WARDROBE')}
    [MICRO-EXPRESSION]: {get('MICRO_EXPRESSION')}
    [ACTION & MOVEMENT]: {get('ACTION')}
    [PROPS IN USE]: {get('PROPS')}
    [LOCATION & SETTING]: {get('LOCATION')}

    --- TECHNICAL & CAPTURE SPECS ---
    [CAPTURE INTENT]: {get('CAPTURE_INTENT')}
    [CAMERA DEVICE]: {get('CAMERA_DEVICE')}
    [LENS & FRAMING]: {get('LENS_SPECS')} | {get('COMPOSITION_FRAMING')}
    [TIME & WEATHER]: {get('TIME_OF_DAY')} with {get('WEATHER')}
    [LIGHTING BEHAVIOR]: {get('LIGHTING_BEHAVIOR')}
    [COLOUR SIMULATION]: {get('COLOUR_SIMULATION')}
{additional_section}

    FORMAT RULES:
    1. Detail the subject's exact micro-expression ({get('MICRO_EXPRESSION')}) under ### Subject.
    2. Incorporate the capture intent ({get('CAPTURE_INTENT')}) into the framing and aesthetic description under ### Camera and ### Scene.
    3. Weave the specific time ({get('TIME_OF_DAY')}) and weather ({get('WEATHER')}) into the environmental atmosphere and light falloff.
    """
