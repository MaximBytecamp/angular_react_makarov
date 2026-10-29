"""Обрезка кадров главы 2.4: читает img/raw, кладёт обрезанные в img/.

Терминал обрезается по доле высоты, у страниц браузера снизу убирается пустой фон.

    python3 tools/crop_24.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/24-sobstvennyy-huk/img"
SHARE = {"11-lint-return": 0.64}
EDITOR = {"01-hook-load", "02-app-load", "04-hook-full", "05-app-final", "07-header-hook", "10-ranniy-return"}
CONSOLE = {"08-network-chetyre", "12-gotovo-oshibka"}
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
