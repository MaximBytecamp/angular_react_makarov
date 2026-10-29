"""Обрезка кадров главы 2.2: читает img/raw, кладёт обрезанные в img/.

Терминал — по доле высоты. Ответы API и консоль — снизу по пустому фону
(цвет фона берётся из нижнего левого угла кадра). Панель PocketBase остаётся целой.

    python3 tools/crop_22.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/22-pocketbase/img"
SHARE = {"03-compose-ps": 0.3, "04-superuser": 0.2}
TRIM = {"13-api-403", "15-api-list", "16-console-gotovo", "17-console-seed", "18-console-title"}


def trim_bottom(im: Image.Image, margin: int = 30) -> Image.Image:
    rgb = im.convert("RGB")
    bg = rgb.getpixel((5, rgb.height - 5))
    box = ImageChops.difference(rgb, Image.new("RGB", rgb.size, bg)).getbbox()
    return rgb.crop((0, 0, rgb.width, min(rgb.height, box[3] + margin))) if box else rgb


for raw in sorted((IMG / "raw").glob("*.png")):
    im = Image.open(raw)
    if raw.stem in SHARE:
        im = im.crop((0, 0, im.width, int(im.height * SHARE[raw.stem])))
    elif raw.stem in TRIM:
        im = trim_bottom(im)
    im.convert("RGB").save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
