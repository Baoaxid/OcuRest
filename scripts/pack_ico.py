import os
import sys
from pathlib import Path
from PIL import Image

def build_pixel_art_ico(source_png: str, target_ico: str) -> None:
    src_path = Path(source_png)
    dst_path = Path(target_ico)

    if not src_path.exists():
        print(f"[Error] Source file not found: {src_path}")
        sys.exit(1)

    img = Image.open(src_path).convert("RGBA")

    # Standard Windows ICO resolution tiers
    ico_resolutions = [16, 24, 32, 48, 64, 128, 256]
    image_layers = []

    for res in ico_resolutions:
        # Use NEAREST resampling to preserve sharp pixel art edges
        resized = img.resize((res, res), Image.Resampling.NEAREST)
        image_layers.append(resized)

    # Save multi-resolution ICO file
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    image_layers[0].save(
        dst_path,
        format="ICO",
        sizes=[(res, res) for res in ico_resolutions],
        append_images=image_layers[1:]
    )
    print(f"[Success] Multi-resolution pixel art icon generated at: {dst_path}")

if __name__ == "__main__":
    SOURCE = "assets/icon_raw.png"
    TARGET = "assets/icon.ico"
    build_pixel_art_ico(SOURCE, TARGET)
