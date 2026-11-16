"""Обрезка кадров главы 4.4: читает img/raw, кладёт обрезанные в img/.

У кадров терминала снизу убирается пустая часть панели, у страниц браузера — пустой фон.

    python3 tools/crop_44.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/44-angular/img"
TERMINAL = {"09-ng-serve", "14-ng-test", "15-ng-build"}
CONSOLE = set()
TOP = {}
BOTTOM = {"01-ng-new": 900}
PAGE_BG = (245, 246, 249)


def trim_bottom(im: Image.Image, bg: tuple, margin: int, box=None) -> Image.Image:
    area = im.convert("RGB").crop(box or (0, 0, im.width, im.height))
    diff = ImageChops.difference(area, Image.new("RGB", area.size, bg)).point(lambda v: 255 if v > 24 else 0)
    found = diff.getbbox()
    top = box[1] if box else 0
    bottom = min(im.height, top + found[3] + margin) if found else im.height
    return im.crop((0, 0, im.width, bottom))


for raw in sorted((IMG / "raw").glob("*.png")):
    im = Image.open(raw)
    if raw.stem in TERMINAL:
        # Текст терминала — правее проводника и ниже заголовков панели.
        bg = im.convert("RGB").getpixel((im.width - 300, im.height - 200))
        im = trim_bottom(im, bg, 70, (720, 140, im.width - 300, im.height - 70))
        im = im.crop((0, 0, im.width, max(im.height, 560)))
    elif raw.stem in BOTTOM:
        im = im.crop((0, 0, im.width, BOTTOM[raw.stem]))
    elif raw.stem in TOP:
        im = im.crop((0, TOP[raw.stem], im.width, im.height))
    elif im.width == 2200 and raw.stem not in CONSOLE:
        im = trim_bottom(im, PAGE_BG, 48)
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
