"""Обрезка кадров главы 2.5: читает img/raw, кладёт обрезанные в img/.

Терминал обрезается по доле высоты, у страниц браузера снизу убирается пустой фон.

    python3 tools/crop_24.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/25-obnovlenie-po-sobytiyam/img"
SHARE = {"02-npm-install": 0.36}
EDITOR = {"03-realtime-ts", "04-hook-dubli", "07-requests-upsert", "08-hook-final", "11-panel-kategoriya", "01-dva-okna-do", "05-dva-okna-dubli", "09-dva-okna-dobavlenie", "10-dva-okna-status"}
CONSOLE = {"06-konsol-key", "13-eventstream"}
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
    elif raw.stem == "12-doska-kategoriya":
        im = im.crop((0, 0, im.width, 2150))
    elif raw.stem not in EDITOR and raw.stem not in CONSOLE:
        im = trim_bottom(im)
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
