"""Обрезка кадров главы 2.3: читает img/raw, кладёт обрезанные в img/.

Терминал обрезается по доле высоты, у страниц браузера снизу убирается пустой фон.

    python3 tools/crop_23.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/23-zagruzka/img"
SHARE = {"09-stop": 0.24, "13-start": 0.24}
EDITOR = {"01-api-ts", "02-requests-ts", "03-app-load", "11-app-error", "15-api-full", "16-app-final", "19-panel"}
CONSOLE = {"05-zagruzka", "06-network-dva", "10-vechnaya-zagruzka"}
PAGE_BG = (246, 247, 249)


def trim_bottom(im: Image.Image, margin: int = 48) -> Image.Image:
    bg = Image.new("RGB", im.size, PAGE_BG)
    box = ImageChops.difference(im.convert("RGB"), bg).getbbox()
    bottom = min(im.height, box[3] + margin) if box else im.height
    return im.crop((0, 0, im.width, bottom))


for raw in sorted((IMG / "raw").glob("*.png")):
    im = Image.open(raw)
    if raw.stem in SHARE:
        im = im.crop((0, 0, im.width, int(im.height * SHARE[raw.stem])))
    elif raw.stem not in EDITOR and raw.stem not in CONSOLE:
        im = trim_bottom(im)
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
