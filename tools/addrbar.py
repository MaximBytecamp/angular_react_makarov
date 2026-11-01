"""Полоса адреса над кадром страницы: headless Chromium снимает страницу без рамки браузера.

В полосе — адрес, который открыт на странице в момент снимка (page.url без http://).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TEXT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)


def _arrow(d: ImageDraw.ImageDraw, x: int, y: int, left: bool) -> None:
    # Стрелка «назад» или «вперёд» в масштабе 2×.
    s = -1 if left else 1
    d.line((x - 11 * s, y, x + 11 * s, y), fill="#5f6368", width=4)
    d.line((x + 11 * s, y, x + 2 * s, y - 9), fill="#5f6368", width=4)
    d.line((x + 11 * s, y, x + 2 * s, y + 9), fill="#5f6368", width=4)


def add(path: Path, url: str) -> None:
    im = Image.open(path).convert("RGB")
    k = im.width // 1100 or 1
    h = 52 * k
    out = Image.new("RGB", (im.width, im.height + h), "#e8eaed")
    d = ImageDraw.Draw(out)
    cy = h // 2
    _arrow(d, 22 * k, cy, True)
    _arrow(d, 54 * k, cy, False)
    d.arc((76 * k, cy - 9 * k, 94 * k, cy + 9 * k), 40, 330, fill="#5f6368", width=4)
    d.rounded_rectangle((110 * k, 8 * k, im.width - 16 * k, h - 8 * k), radius=18 * k, fill="#ffffff")
    shown = url.removeprefix("http://")
    host, _, rest = shown.partition("/")
    d.text((128 * k, cy), host, fill="#202124", font=TEXT, anchor="lm")
    w = d.textlength(host, font=TEXT)
    d.text((128 * k + w, cy), "/" + rest, fill="#3c4043", font=TEXT, anchor="lm")
    d.line((0, h - 1, im.width, h - 1), fill="#c4c7cf", width=2)
    out.paste(im, (0, h))
    out.save(path)
