import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Paths
MODELS_DIR = BASE_DIR / "backend" / "models"
WORKFLOWS_DIR = BASE_DIR / "workflows"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Local LLM (quantized GGUF)
LLM_MODEL_PATH = MODELS_DIR / "dolphin-2.9-llama3-8b.Q4_K_M.gguf"
# Alternative uncensored: "Llama-3.2-8X4B-MOE-V2-Q4_K_M.gguf"

# ComfyUI settings
COMFYUI_URL = "http://127.0.0.1:8188"  # default local
COLAB_COMFYUI_URL = None  # will be set by colab_bridge if available

# Model names for workflows
SD_MODEL = "sd_xl_base_1.0.safetensors"
FLUX_MODEL = "flux1-dev.safetensors"
WAN_MODEL = "Wan2.1-T2V-14B-Q4_K_M.gguf"  # quantized Wan

# Negative prompt (shared)
NEGATIVE_PROMPT = (
    "bad hands, mutated hands, deformed hands, ugly hands, "
    "extra fingers, missing fingers, fused fingers, "
    "bad anatomy, deformed anatomy, disproportionate body, "
    "low quality, worst quality, blurry, pixelated"
)