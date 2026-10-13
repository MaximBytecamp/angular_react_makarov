"""Обрезка кадров главы 1.1.

Сценарий съёмки (tools/shots_11.py) пишет исходные кадры в img/raw/ (в репозиторий
не попадает). Этот скрипт только читает их и кладёт в img/ обрезанные:
у терминала убирается пустое поле под последней строкой, у страниц в браузере —
нижняя часть, которая в тексте не разбирается.

    python3 tools/crop_11.py
"""
import shutil
from pathlib import Path

from PIL import Image

IMG = Path(__file__).resolve().parent.parent / "temy/11-node-npm-vite/img"
RAW = IMG / "raw"

# Кадры терминала: обрезка по последней строке текста.
TERMINAL = ["01-node-npm-versii", "02-create-ok-to-proceed", "03-create-linter",
            "04-create-install-now", "05-create-done", "06-npm-install", "07-npm-run-dev"]
# Кадры с заданной долей высоты.
SHARE = {"08-stranica-vite": 0.62, "08b-schetchik-3": 0.62, "12-stranica-hmr": 0.62,
         "14-stranica-karkas": 0.36, "13-app-karkas": 0.52}


def text_bottom(im: Image.Image) -> int:
    """Нижняя граница текста в области терминала: строки, где есть тёмные точки."""
    gray = im.convert("L")
    w, h = gray.size
    left, right = int(w * 0.05), int(w * 0.85)
    top = int(h * 0.12)
    bottom = top
    px = gray.load()
    for y in range(top, int(h * 0.95)):
        if any(px[x, y] < 140 for x in range(left, right, 3)):
            bottom = y
    return bottom


def text_right(im: Image.Image) -> int:
    """Правая граница текста в области терминала (ниже строки вкладок панели)."""
    gray = im.convert("L")
    w, h = gray.size
    px = gray.load()
    right = 0
    for y in range(130, int(h * 0.97), 2):
        for x in range(int(w * 0.85), int(w * 0.05), -2):
            if px[x, y] < 140:
                right = max(right, x)
                break
    return right


def main() -> None:
    for raw in sorted(RAW.glob("*.png")):
        im = Image.open(raw)
        name = raw.stem
        if name in TERMINAL:
            right = max(int(im.width * 0.5), text_right(im) + 110)
            # Строка заголовка окна (около 60 точек сверху) отрезается: на узком кадре
            # название папки в ней оказывалось разрезанным пополам.
            im = im.crop((0, 62, min(im.width, right), min(im.height, text_bottom(im) + 70)))
        elif name in SHARE:
            im = im.crop((0, 0, im.width, int(im.height * SHARE[name])))
        im.save(IMG / raw.name, optimize=True)
        print(f"  {raw.name}: {im.width}×{im.height}")


if __name__ == "__main__":
    main()
