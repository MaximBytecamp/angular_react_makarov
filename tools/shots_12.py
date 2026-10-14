"""Кадры главы 1.2: JSX и компоненты.

Продолжает проект zayavki из главы 1.1 (/private/tmp/student/react-kurs/zayavki).
Профиль редактора и Node 24 — те же, что в tools/shots_11.py. Код компонентов
берётся из tools/code12: эти файлы проверены сборкой и линтером, и те же тексты
стоят в блоках главы.

    python3 tools/shots_12.py reset      # вернуть проект к заготовке из главы 1.1
    python3 tools/shots_12.py all        # все кадры по порядку
"""
import asyncio
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/12-jsx-i-komponenty/img/raw"
CODE = Path(__file__).parent / "code12"
PROJECT = s11.PROJECT
SRC = PROJECT / "src"

# App.tsx после первого шага (подключена только шапка) и шапка без общей обёртки
# для опыта с ошибкой — те же файлы, что в блоках главы.
APP_HEADER_ONLY = (CODE / "App-shapka.tsx").read_text()
HEADER_BROKEN = (CODE / "Header-bez-obertki.tsx").read_text()


def reset() -> None:
    """Проект в состоянии конца главы 1.1."""
    (SRC / "App.tsx").write_text(s11.KARKAS_APP)
    (SRC / "index.css").write_text(s11.KARKAS_CSS)
    shutil.rmtree(SRC / "components", ignore_errors=True)
    print("проект возвращён к заготовке")


async def explorer_button(ed: cdp.Editor, label: str) -> None:
    """Кнопка в заголовке проводника (New File… / New Folder…): видна только под курсором."""
    head = await ed.rect(".explorer-folders-view, .pane-header[aria-label*='Explorer Section']")
    pane = await ed.rect(".split-view-view .pane-header")
    if pane:
        await ed.move(pane[0] + 60, pane[1] + pane[3] / 2, 0.6)
    r = await ed.rect(f"a.action-label[aria-label^='{label}']")
    if not r:
        raise RuntimeError(f"нет кнопки {label}")
    await ed.click(r[0] + r[2] / 2, r[1] + r[3] / 2, 1.0)


async def select_in_tree(ed: cdp.Editor, name: str) -> None:
    """Щелчок по строке дерева проводника с заданным именем."""
    r = await ed.js(f"""(() => {{
      const row = [...document.querySelectorAll('.explorer-folders-view .monaco-list-row')]
        .find(e => e.getAttribute('aria-label') === {name!r} || e.innerText.trim() === {name!r});
      if (!row) return null;
      const b = row.getBoundingClientRect();
      return [b.x, b.y, b.width, b.height];
    }})()""")
    if not r:
        raise RuntimeError(f"нет строки {name}")
    await ed.click(r[0] + 80, r[1] + r[3] / 2, 0.8)


async def all_frames() -> None:
    reset()
    cdp.launch(str(s11.WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1240, 780)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki && npm run dev", 6)
        await ed.palette("View: Close Panel", 1)
        await ed.palette("View: Show Explorer", 1.2)
        await s11.open_file(ed, "zayavki/src/App.tsx")
        await ed.palette("File: Reveal Active File in Explorer View", 1.2)

        # Шаг 1: папка components внутри src.
        await select_in_tree(ed, "src")
        await explorer_button(ed, "New Folder")
        await ed.type("components", 0.8)
        await ed.shot(str(IMG / "01-novaya-papka.png"))
        await ed.key("Enter", 1.5)

        # Шаг 2: файл Header.tsx внутри components.
        await select_in_tree(ed, "components")
        await explorer_button(ed, "New File")
        await ed.type("Header.tsx", 0.8)
        await ed.shot(str(IMG / "02-novyy-fayl.png"))
        await ed.key("Enter", 2.0)
        (SRC / "components/Header.tsx").write_text((CODE / "Header.tsx").read_text())
        await asyncio.sleep(1.5)
        await ed.palette("File: Revert File", 1.2)
        await ed.shot(str(IMG / "03-header-tsx.png"))

        # Шаг 3: шапка подключена в App.tsx.
        (SRC / "App.tsx").write_text(APP_HEADER_ONLY)
        await asyncio.sleep(2)
        page = await s11.browser_shot(IMG / "04-stranica-header.png")

        # Ошибка: два корневых элемента в Header.
        (SRC / "components/Header.tsx").write_text(HEADER_BROKEN)
        await asyncio.sleep(2)
        await page.reload()
        await s11.browser_shot(IMG / "05-oshibka-dva-kornya.png", page=page)
        (SRC / "components/Header.tsx").write_text((CODE / "Header.tsx").read_text())
        await asyncio.sleep(2)

        # Шаги 4–6: форма, карточка, App целиком — страница без новых стилей.
        for name in ("RequestForm.tsx", "RequestCard.tsx"):
            (SRC / "components" / name).write_text((CODE / name).read_text())
        (SRC / "App.tsx").write_text((CODE / "App.tsx").read_text())
        await asyncio.sleep(2.5)
        await page.reload()
        await s11.browser_shot(IMG / "06-stranica-bez-stiley.png", page=page)

        # Шаг 7: стили.
        (SRC / "index.css").write_text((CODE / "index.css").read_text())
        await asyncio.sleep(2)
        await s11.browser_shot(IMG / "07-doska-gotova.png", page=page)

        await s11.open_file(ed, "zayavki/src/App.tsx")
        await ed.palette("File: Revert File", 1.0)
        await ed.palette("File: Reveal Active File in Explorer View", 1.2)
        await ed.shot(str(IMG / "08-provodnik-app.png"))


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name == "reset":
        reset()
    elif name == "all":
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: reset, all")
