def enrich_scene_to_prompt(scene: dict, style: str = "anime") -> dict:
    """Convert a scene dict to a detailed SD/Flux prompt."""
    char_desc = scene.get("character_description", "a character")
    location = scene.get("location", "unknown")
    action = scene.get("action", "standing")
    emotion = scene.get("emotion", "neutral")
    composition = scene.get("composition", "cinematic shot")
    lighting = scene.get("lighting", "dramatic lighting")

    positive = (
        f"{style} style, high quality, detailed, "
        f"character: {char_desc}, "
        f"{action}, {emotion} expression, "
        f"location: {location}, "
        f"{composition}, {lighting}"
    )
    # Use global negative prompt
    from .config import NEGATIVE_PROMPT
    return {
        "positive": positive,
        "negative": NEGATIVE_PROMPT
    }