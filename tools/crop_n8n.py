"""Обрезка кадров страницы «Автоматизация»: читает img/raw, кладёт обрезанные в img/.

Ответ getUpdates и страница доски обрезаются снизу по пустому фону,
терминал с docker compose — по доле высоты, кадры n8n остаются целыми.

    python3 tools/crop_n8n.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/18-avtomatizaciya/img"
SHARE = {"a02-compose-up": 0.4}
TRIM = {"a11-getupdates": (255, 255, 255), "a15-otpravleno": (246, 247, 249)}


def trim_bottom(im: Image.Image, bg: tuple[int, int, int], margin: int = 40) -> Image.Image:
    box = ImageChops.difference(im.convert("RGB"), Image.new("RGB", im.size, bg)).getbbox()
    return im.crop((0, 0, im.width, min(im.height, box[3] + margin))) if box else im


for raw in sorted((IMG / "raw").glob("*.png")):
    im = Image.open(raw)
    if raw.stem in SHARE:
        im = im.crop((0, 0, im.width, int(im.height * SHARE[raw.stem])))
    elif raw.stem in TRIM:
        im = trim_bottom(im, TRIM[raw.stem])
    im.convert("RGB").save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
