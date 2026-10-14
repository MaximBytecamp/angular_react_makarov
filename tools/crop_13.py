"""Обрезка кадров главы 1.3: читает img/raw, кладёт обрезанные в img/ (доля высоты).

    python3 tools/crop_13.py
"""
from pathlib import Path

from PIL import Image

IMG = Path(__file__).resolve().parent.parent / "temy/13-props/img"
SHARE = {"01-requestcard-props": 0.73, "05-requestcard-status": 0.78,
         "03-oshibka-room": 0.74, "06-oshibka-status": 0.74,
         "02-tri-zayavki": 0.74, "04-stranica-bez-room": 0.74, "07-doska-props": 0.74}

for raw in sorted((IMG / "raw").glob("*.png")):
    im = Image.open(raw)
    im = im.crop((0, 0, im.width, int(im.height * SHARE.get(raw.stem, 1.0))))
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
