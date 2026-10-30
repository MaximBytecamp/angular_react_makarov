"""Обрезка кадров страницы «ИИ-диспетчер»: читает img/raw, кладёт обрезанные в img/.

Терминал обрезается по доле высоты, у страниц доски снизу убирается пустой фон.
Снимки Telegram (b18–b20) кладутся в img/ сразу, их здесь нет.

    python3 tools/crop_28.py
"""
from pathlib import Path

from PIL import Image, ImageChops

IMG = Path(__file__).resolve().parent.parent / "temy/28-ii-dispetcher/img"
SHARE = {"b03-compose-up": 0.5, "b04-ollama-list": 0.2, "b05-ollama-run": 0.28}
PAGE = {"b14-doska-otpravleno", "b17-doska-v-rabote"}
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
    elif raw.stem in PAGE:
        im = trim_bottom(im)
    im.save(IMG / raw.name, optimize=True)
    print(f"  {raw.name}: {im.width}×{im.height}")
