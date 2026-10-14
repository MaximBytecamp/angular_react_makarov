"""Вставляет в главу блоки кода из проверенных файлов (маркеры <!--CODE …-->, см. hl.py).

    python3 tools/build.py temy/13-props
"""
import sys
from pathlib import Path

from hl import ROOT, expand

for arg in sys.argv[1:]:
    page = ROOT / arg / "index.html"
    print(arg, "блоков:", expand(page))
