"""Кадры главы 1.3: props.

Продолжает проект zayavki после главы 1.2 (tools/shots_12.py all). Код — из tools/code13.

    python3 tools/shots_13.py reset   # проект в состоянии конца главы 1.2
    python3 tools/shots_13.py all
"""
import asyncio
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/13-props/img/raw"
C12 = Path(__file__).parent / "code12"
CODE = Path(__file__).parent / "code13"
SRC = s11.PROJECT / "src"


def reset() -> None:
    """Состояние конца главы 1.2: три компонента, App.tsx и стили."""
    (SRC / "components").mkdir(exist_ok=True)
    for name in ("Header.tsx", "RequestForm.tsx", "RequestCard.tsx"):
        shutil.copy(C12 / name, SRC / "components" / name)
    shutil.copy(C12 / "App.tsx", SRC / "App.tsx")
    shutil.copy(C12 / "index.css", SRC / "index.css")
    print("проект в состоянии конца главы 1.2")


def put(src_name: str, dest: str) -> None:
    shutil.copy(CODE / src_name, SRC / dest)


async def problems(ed: cdp.Editor, show: bool) -> None:
    """Панель Problems с ошибками TypeScript внизу окна."""
    if show:
        await ed.palette("View: Focus Problems (Errors, Warnings, Infos)", 2.5)
        # Панель могла остаться развёрнутой на всё окно со съёмки главы 1.1:
        # тогда редактор с подчёркнутой строкой не виден.
        editor_h = await ed.js("document.querySelector('.part.editor').getBoundingClientRect().height")
        if editor_h < 150:
            await ed.palette("View: Toggle Maximized Panel", 1.5)
    else:
        await ed.palette("View: Close Panel", 1)


async def go_line(ed: cdp.Editor, line: int) -> None:
    """Курсор на строку: ошибочная строка оказывается в середине видимой части редактора."""
    await ed.palette("Go to Line/Column...", 1.0)
    await ed.paste(str(line), 0.5)
    await ed.key("Enter", 1.0)


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

        # Шаг 1: RequestCard получает props.
        put("RequestCard-props.tsx", "components/RequestCard.tsx")
        await s11.open_file(ed, "zayavki/src/components/RequestCard.tsx")
        await ed.palette("File: Revert File", 1.0)
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await ed.shot(str(IMG / "01-requestcard-props.png"))

        # Шаг 2: App передаёт три разные заявки.
        put("App-props.tsx", "App.tsx")
        await asyncio.sleep(2)
        page = await s11.browser_shot(IMG / "02-tri-zayavki.png")

        # Опыт 1: забытый room — ошибка в редакторе, страница открывается.
        put("App-bez-room.tsx", "App.tsx")
        await s11.open_file(ed, "zayavki/src/App.tsx")
        await ed.palette("File: Revert File", 1.0)
        await asyncio.sleep(6)
        await go_line(ed, 19)
        await problems(ed, True)
        await ed.shot(str(IMG / "03-oshibka-room.png"))
        await problems(ed, False)
        await s11.browser_shot(IMG / "04-stranica-bez-room.png", page=page)

        # Шаг 3: статус из трёх значений и значение по умолчанию.
        put("RequestCard.tsx", "components/RequestCard.tsx")
        put("App.tsx", "App.tsx")
        await s11.open_file(ed, "zayavki/src/components/RequestCard.tsx")
        await ed.palette("File: Revert File", 1.0)
        await ed.shot(str(IMG / "05-requestcard-status.png"))

        # Опыт 2: опечатка в статусе.
        put("App-opechatka.tsx", "App.tsx")
        await s11.open_file(ed, "zayavki/src/App.tsx")
        await ed.palette("File: Revert File", 1.0)
        await asyncio.sleep(6)
        await go_line(ed, 29)
        await problems(ed, True)
        await ed.shot(str(IMG / "06-oshibka-status.png"))
        await problems(ed, False)

        # Итог главы.
        put("App.tsx", "App.tsx")
        await ed.palette("File: Revert File", 1.0)
        await asyncio.sleep(2)
        await page.reload()
        await s11.browser_shot(IMG / "07-doska-props.png", page=page)


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name == "reset":
        reset()
    elif name == "all":
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: reset, all")
