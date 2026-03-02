from llama_cpp import Llama
import json
from . import config

class StoryGenerator:
    def __init__(self):
        self.llm = Llama(
            model_path=str(config.LLM_MODEL_PATH),
            n_ctx=4096,
            n_gpu_layers=-1,  # use GPU if available
            verbose=False
        )

    def generate(self, prompt: str, genre: str = "fantasy") -> dict:
        system_msg = """You are a creative writer. Generate a story with:
        - title
        - characters (list of objects with name, description)
        - scenes (list of objects with location, action, emotion, dialogue)
        Output valid JSON only."""
        user_msg = f"Genre: {genre}\nPrompt: {prompt}"

        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            response_format={"type": "json_object"},
            temperature=0.8,
            max_tokens=2048
        )
        content = response["choices"][0]["message"]["content"]
        return json.loads(content)