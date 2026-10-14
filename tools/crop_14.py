"""Обрезка кадров главы 1.4: читает img/raw, кладёт обрезанные в img/ (доля высоты).

    python3 tools/crop_14.py
"""
from pathlib import Path

from PIL import Image

IMG = Path(__file__).resolve().parent.parent / "temy/14-sostoyanie-i-sobytiya/img"
SHARE = {"04-lint-let": 0.4, "06-sostoyanie-kartochek": 0.93, "09-schetchik-1": 0.97, "10-schetchik-0": 0.97,
         "02-konsol-nazhatiya": 0.88, "03-peremennaya-let": 0.86}
# Страница с ошибкой пустая: от неё остаётся полоса сверху, под ней консоль (склейка на 1036 px).
BLANK = {"07-vyzov-vmesto-peredachi": (240, 1036, 1400)}

for raw in sorted((IMG / "raw").glob("*.png")):
    im = Image.open(raw)
    if raw.stem in BLANK:
        keep, seam, end = BLANK[raw.stem]
        out = Image.new("RGB", (im.width, keep + end - seam))
        out.paste(im.crop((0, 0, im.width, keep)), (0, 0))
        out.paste(im.crop((0, seam, im.width, end)), (0, keep))
        im = out
    else:
        im = im.crop((0, 0, im.width, int(im.height * SHARE.get(raw.stem, 1.0))))
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
