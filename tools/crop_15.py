"""Обрезка кадров главы 1.5: читает img/raw, кладёт обрезанные в img/.

Терминал с линтером обрезается по доле высоты. У страниц браузера снизу
убирается пустой фон: кадр заканчивается чуть ниже последнего блока.

    python3 tools/crop_15.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/15-spiski-i-usloviya/img"
SHARE = {"05-lint-key": 0.3, "08-lint-mutaciya": 0.3}
EDITOR = {"01-requests-ts", "02-app-map", "10-card-uslovie", "14-app-filtr"}
CONSOLE = {"04-konsol-key", "06-konsol-chisto", "07-mutaciya"}
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
    elif raw.stem in CONSOLE:
        im = im.crop((0, 0, im.width, int(im.height * 0.9)))
    elif raw.stem not in EDITOR:
        im = trim_bottom(im)
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
