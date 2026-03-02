from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import os
from pathlib import Path

from . import config
from .story_generator import StoryGenerator
from .scene_parser import parse_scenes
from .prompt_enricher import enrich_scene_to_prompt
from .comfyui_client import ComfyUIClient
from .comic_layout import create_comic_page
from .colab_bridge import use_colab_if_available

app = FastAPI(title="AI Creative Studio")

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

# Initialize components
story_gen = StoryGenerator()
comfy_client = use_colab_if_available()  # auto-detects Colab

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate-story")
async def api_generate_story(prompt: str = Form(...), genre: str = Form("fantasy")):
    try:
        story = story_gen.generate(prompt, genre)
        return JSONResponse({"success": True, "story": story})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/generate-comic")
async def api_generate_comic(request: Request):
    data = await request.json()
    story = data.get("story")
    if not story:
        raise HTTPException(400, "Story missing")

    # 1. Parse scenes
    scenes = parse_scenes(story)

    # 2. Enrich each scene to prompts
    workflows = []
    for scene in scenes:
        prompts = enrich_scene_to_prompt(scene, style=data.get("style", "anime"))
        # Load base SDXL workflow and inject prompts
        wf = comfy_client.load_workflow("sdxl_workflow")
        # This depends on your workflow structure – you'll need to modify node inputs
        # Example: assume node 6 is CLIPTextEncode (positive) and node 7 is negative
        wf["6"]["inputs"]["text"] = prompts["positive"]
        wf["7"]["inputs"]["text"] = prompts["negative"]
        workflows.append(wf)

    # 3. Generate images via ComfyUI
    image_files = comfy_client.generate_images(workflows)

    # 4. Assemble into comic page (simple 2x2 grid for demo)
    # For now, just take first 4 images
    panel_images = [str(config.OUTPUTS_DIR / f) for f in image_files[:4]]
    # Mock dialogue texts (in real app, extract from scene)
    texts = [scene.get("dialogue", "") for scene in scenes[:4]]
    page_path = create_comic_page(panel_images, texts)

    return JSONResponse({
        "success": True,
        "images": image_files,
        "comic_page": page_path
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)