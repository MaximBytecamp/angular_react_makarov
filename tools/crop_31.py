"""Обрезка кадров главы 3.1: читает img/raw, кладёт обрезанные в img/.

Терминал обрезается по доле высоты, у страниц браузера снизу убирается пустой фон.

    python3 tools/crop_31.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/31-marshrutizaciya/img"
SHARE = {"02-npm-install": 0.36}
CONSOLE = {"09-abc-pusto", "14-a-network", "16-navlink-network"}
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
    elif im.width == 2200 and raw.stem not in CONSOLE:
        im = trim_bottom(im)
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
