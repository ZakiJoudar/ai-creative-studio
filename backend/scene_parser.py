import json
from . import config

# Use the same LLM instance or a separate one
from .story_generator import StoryGenerator
llm = StoryGenerator().llm  # reuse if you prefer

def parse_scenes(story_json: dict) -> list:
    """Takes the full story JSON and returns a list of enriched scenes."""
    story_text = story_json.get("story", "")  # adjust based on your output
    system_msg = """You are a scene analyzer. Break the story into scenes.
    For each scene output:
    - scene_number
    - location
    - characters_present (list of names)
    - action
    - emotion
    - narration (if any)
    - dialogue (if any)
    Output a JSON array of scenes."""
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": story_text}
        ],
        response_format={"type": "json_object"},
        temperature=0.5,
        max_tokens=2048
    )
    scenes = json.loads(response["choices"][0]["message"]["content"])
    return scenes  # expected to be a list