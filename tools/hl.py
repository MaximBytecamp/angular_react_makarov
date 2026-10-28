"""Подсветка кода для блоков справочника и вставка файлов в главу.

В главе блок кода отмечается парой комментариев:

    <!--CODE tools/code12/Header.tsx | zayavki/src/components/Header.tsx-->
    <!--/CODE-->

Слева от черты — файл-источник (путь от корня справочника), справа — подпись блока.
Необязательные ключи после второй черты: `read` (блок для чтения, без кнопки
«копировать»), `lines=3-9` (взять только эти строки файла), `pins=5:1,9:2` (номерные
метки в конце строк 5 и 9 для пояснений списком .anno; такой блок — только для чтения),
`bare` (только <pre class="trace__code"> для пошагового разбора .trace; номера строк
в разборе — как в файле).
`expand()` заменяет содержимое между комментариями на готовый <figure class="code">,
поэтому повторный запуск обновляет блоки, а не дублирует их.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KW = {"import", "from", "export", "default", "function", "return", "const", "let", "type",
      "true", "false", "null", "undefined", "if", "else", "new"}

TSX = re.compile(r"""
    (?P<c>//[^\n]*|/\*.*?\*/)
  | (?P<s>'[^'\n]*'|"[^"\n]*"|`[^`]*`)
  | (?P<g>(?<=\w)<[A-Z]\w*>(?=\())
  | (?P<t></?[A-Za-z][\w.]*|/?>|<>|</>)
  | (?P<a>\b[a-zA-Z-]+(?==))
  | (?P<n>\b\d+(?:\.\d+)?\b)
  | (?P<w>\b[A-Za-z_]\w*\b)
""", re.X | re.S)

CSS = re.compile(r"""
    (?P<c>/\*.*?\*/)
  | (?P<s>'[^'\n]*'|"[^"\n]*")
  | (?P<a>(?<=[\s{;])[a-z-]+(?=\s*:))
  | (?P<n>\#[0-9a-fA-F]{3,8}\b|\b\d+(?:\.\d+)?(?:px|%|em|rem|fr)?\b)
""", re.X | re.S)


def highlight(src: str, lang: str) -> str:
    rx = CSS if lang == "css" else TSX
    out, pos = [], 0
    for m in rx.finditer(src):
        out.append(html.escape(src[pos:m.start()], quote=False))
        kind, text = m.lastgroup, html.escape(m.group(), quote=False)
        if kind == "g":
            out.append(text)
        elif kind == "w":
            out.append(f'<span class="k">{text}</span>' if m.group() in KW
                       else (f'<span class="f">{text}</span>' if src[m.end():m.end() + 1] == "(" else text))
        else:
            out.append(f'<span class="{kind}">{text}</span>')
        pos = m.end()
    out.append(html.escape(src[pos:], quote=False))
    return "".join(out)


def figure(spec: str) -> str:
    parts = [p.strip() for p in spec.split("|")]
    path, caption = parts[0], parts[1]
    opts = parts[2].split() if len(parts) > 2 else []
    text = (ROOT / path).read_text()
    start = 1
    for o in opts:
        if o.startswith("lines="):
            a, b = map(int, o[6:].split("-"))
            text = "\n".join(text.split("\n")[a - 1:b])
            start = a
    text = text.rstrip("\n")
    lang = "css" if path.endswith(".css") else "tsx"
    code = highlight(text, lang)
    pins = dict(p.split(":") for o in opts if o.startswith("pins=") for p in o[5:].split(","))
    if pins:
        rows = code.split("\n")
        for line, num in pins.items():
            rows[int(line) - start] += f'  <span class="pin">{num}</span>'
        code = "\n".join(rows)
    if "bare" in opts:
        return f'<pre class="trace__code" data-start="{start}">{code}</pre>'
    attr = " data-read" if "read" in opts or pins else ""
    return (f'<figure class="code"{attr}><figcaption><span>{html.escape(caption)}</span></figcaption>'
            f'<pre>{code}</pre></figure>')


def expand(chapter: Path) -> int:
    s = chapter.read_text()
    n = 0

    def rep(m):
        nonlocal n
        n += 1
        return f"<!--CODE {m.group(1)}-->{figure(m.group(1))}<!--/CODE-->"

    s = re.sub(r"<!--CODE (.*?)-->.*?<!--/CODE-->", rep, s, flags=re.S)
    chapter.write_text(s)
    return n
