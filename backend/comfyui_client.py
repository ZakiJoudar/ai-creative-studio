import requests
import json
import time
import os
from . import config

class ComfyUIClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or config.COMFYUI_URL
        self.client_id = "ai-creative-studio"

    def queue_prompt(self, workflow_json: dict) -> str:
        """Submit workflow and return prompt_id."""
        payload = {"prompt": workflow_json, "client_id": self.client_id}
        resp = requests.post(f"{self.base_url}/prompt", json=payload)
        resp.raise_for_status()
        return resp.json()["prompt_id"]

    def get_history(self, prompt_id: str) -> dict:
        """Retrieve generation history (includes output images)."""
        resp = requests.get(f"{self.base_url}/history")
        resp.raise_for_status()
        history = resp.json()
        return history.get(prompt_id, {})

    def wait_for_image(self, prompt_id: str, timeout=120):
        """Poll until image is generated, return list of output filenames."""
        start = time.time()
        while time.time() - start < timeout:
            history = self.get_history(prompt_id)
            if history:
                outputs = history.get("outputs", {})
                images = []
                for node_id, node_out in outputs.items():
                    if "images" in node_out:
                        for img in node_out["images"]:
                            images.append(img["filename"])
                return images
            time.sleep(2)
        raise TimeoutError("Image generation timed out")

    def load_workflow(self, workflow_name: str) -> dict:
        """Load a predefined JSON workflow from disk."""
        path = config.WORKFLOWS_DIR / f"{workflow_name}.json"
        with open(path, "r") as f:
            return json.load(f)

    def generate_images(self, workflows: list) -> list:
        """Submit multiple workflows, return list of output filenames."""
        all_images = []
        for wf in workflows:
            prompt_id = self.queue_prompt(wf)
            images = self.wait_for_image(prompt_id)
            all_images.extend(images)
        return all_images