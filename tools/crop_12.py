"""Обрезка кадров главы 1.2: читает img/raw, кладёт обрезанные в img/.

Для каждого кадра задана доля высоты, которая остаётся. У кадров с полем ввода
в проводнике (01, 02) оставлена только левая часть окна: остальное к шагу не относится.

    python3 tools/crop_12.py
"""
from pathlib import Path

from PIL import Image

IMG = Path(__file__).resolve().parent.parent / "temy/12-jsx-i-komponenty/img"
SHARE = {
    "01-novaya-papka": 0.68, "02-novyy-fayl": 0.68, "03-header-tsx": 0.68,
    "04-stranica-header": 0.36, "05-oshibka-dva-kornya": 0.72,
    "06-stranica-bez-stiley": 1.0, "07-doska-gotova": 0.9, "08-provodnik-app": 0.78,
}

for raw in sorted((IMG / "raw").glob("*.png")):
    im = Image.open(raw)
    share = SHARE.get(raw.stem, 1.0)
    if raw.stem in ("01-novaya-papka", "02-novyy-fayl"):
        im = im.crop((0, 62, 700, int(im.height * share)))
    else:
        im = im.crop((0, 0, im.width, int(im.height * share)))
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
