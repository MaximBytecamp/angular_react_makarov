"""Вставляет в главу 1.2 блоки кода из tools/code12 (проверенные сборкой файлы).

    python3 tools/build_12.py
"""
from pathlib import Path

from hl import expand

ROOT = Path(__file__).resolve().parent.parent
print("блоков:", expand(ROOT / "temy/12-jsx-i-komponenty/index.html"))
