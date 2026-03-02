from PIL import Image, ImageDraw, ImageFont
import os
from . import config

def create_comic_page(panel_images: list, texts: list = None, rows=2, cols=2):
    """Assemble panel images into a grid, add text balloons."""
    if not panel_images:
        return None

    # Assume all panels are same size; we'll resize to common width/height
    panel_w, panel_h = 512, 512  # default, but could detect from first image
    page_width = cols * panel_w
    page_height = rows * panel_h
    page = Image.new("RGB", (page_width, page_height), "white")

    for idx, img_path in enumerate(panel_images):
        if idx >= rows * cols:
            break
        row = idx // cols
        col = idx % cols
        x = col * panel_w
        y = row * panel_h

        img = Image.open(img_path)
        img = img.resize((panel_w, panel_h), Image.LANCZOS)
        page.paste(img, (x, y))

        # Add text balloon if text provided
        if texts and idx < len(texts) and texts[idx]:
            draw = ImageDraw.Draw(page)
            # Simple bubble at bottom of panel
            bbox = draw.textbbox((x+10, y+panel_h-60), texts[idx], font=None)
            draw.rectangle(bbox, fill="white", outline="black")
            draw.text((x+15, y+panel_h-55), texts[idx], fill="black")

    output_path = config.OUTPUTS_DIR / f"comic_page_{int(time.time())}.png"
    page.save(output_path)
    return str(output_path)