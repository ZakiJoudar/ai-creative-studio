import requests
import time
import json
from . import config

COLAB_URL_FILE = config.BASE_DIR / "colab_url.txt"

def detect_colab_comfyui():
    """Check if a Colab ComfyUI tunnel is available."""
    if config.COLAB_COMFYUI_URL:
        return config.COLAB_COMFYUI_URL

    # Try to read from file (written by Colab notebook)
    if COLAB_URL_FILE.exists():
        with open(COLAB_URL_FILE, "r") as f:
            url = f.read().strip()
        # Test connection
        try:
            r = requests.get(f"{url}/system_stats", timeout=5)
            if r.status_code == 200:
                config.COLAB_COMFYUI_URL = url
                return url
        except:
            pass
    return None

def use_colab_if_available():
    """Return ComfyUIClient with appropriate URL."""
    colab_url = detect_colab_comfyui()
    if colab_url:
        from .comfyui_client import ComfyUIClient
        return ComfyUIClient(base_url=colab_url)
    else:
        # fallback to local
        from .comfyui_client import ComfyUIClient
        return ComfyUIClient()