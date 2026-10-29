"""Кадры главы 1.7: сохранение и отправка данных.

Продолжает проект zayavki после главы 1.6. Код — из tools/code17. n8n в этой главе
не запущен: запрос fetch на localhost:5678 не проходит, и это часть опыта.

    python3 tools/shots_17.py reset   # проект в состоянии конца главы 1.6
    python3 tools/shots_17.py all
"""
import asyncio
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_14 as s14  # noqa: E402
import shots_15 as s15  # noqa: E402
import shots_16 as s16  # noqa: E402
from shots_13 import go_line  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/17-sohranenie-i-otpravka/img/raw"
C16 = Path(__file__).parent / "code16"
CODE = Path(__file__).parent / "code17"
SRC = s11.PROJECT / "src"


def reset() -> None:
    """Состояние конца главы 1.6."""
    s16.reset()
    for name in ("App.tsx", "index.css", "requests.ts"):
        shutil.copy(C16 / name, SRC / name)
    for name in ("RequestCard.tsx", "RequestForm.tsx"):
        shutil.copy(C16 / name, SRC / "components" / name)
    for name in ("storage.ts", "notify.ts"):
        (SRC / name).unlink(missing_ok=True)
    print("проект в состоянии конца главы 1.6")


def put(src_name: str, dest: str) -> None:
    shutil.copy(CODE / src_name, SRC / dest)


async def add(br: s15.Browser, title: str, room: str, category: str) -> None:
    await s16.fill(br, title, room, category, "")
    await br.page.get_by_role("button", name="Отправить заявку").click()
    await br.page.wait_for_timeout(800)


async def application_panel(br: s15.Browser) -> None:
    """DevTools: вкладка Application, раздел Local storage для localhost:5173."""
    dt = br.dt
    await dt.set_viewport_size({"width": 1100, "height": 420})
    await dt.get_by_role("tab", name="Application").click()
    await dt.wait_for_timeout(1200)
    await dt.get_by_text("Local storage", exact=True).first.click()
    await dt.wait_for_timeout(400)
    await dt.keyboard.press("ArrowRight")
    await dt.wait_for_timeout(400)
    await dt.keyboard.press("ArrowDown")
    await dt.keyboard.press("Enter")
    await dt.wait_for_timeout(1200)
    # Первая строка таблицы ключей: щелчок по ней показывает значение внизу панели.
    await dt.mouse.click(400, 145)
    await dt.wait_for_timeout(800)


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
        br = s15.Browser()
        await br.start()

        # §1. Опыт: без сохранения новая заявка пропадает после F5.
        await asyncio.sleep(1.5)
        await br.load()
        await br.page.evaluate("localStorage.clear()")
        await add(br, "Не работает звонок", "Вахта", "Компьютер")
        await br.full(IMG / "01-do-perezagruzki.png")
        await br.load()
        await br.full(IMG / "02-posle-perezagruzki.png")

        # §2. localStorage: заявка остаётся.
        put("storage.ts", "storage.ts")
        put("App-storage.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/storage.ts")
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await go_line(ed, 1)
        await ed.shot(str(IMG / "03-storage-ts.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await add(br, "Не работает звонок", "Вахта", "Компьютер")
        await br.page.locator("button", has_text="Взять в работу").nth(1).click()
        await br.load()
        await br.full(IMG / "04-sohranilos.png")
        await br.load()
        await br.devtools()
        await application_panel(br)
        await br.shot(IMG / "05-application.png", console=True)

        # §3–4. fetch на адрес n8n, который не запущен.
        put("index.css", "index.css")
        put("notify.ts", "notify.ts")
        put("App.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/notify.ts")
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await go_line(ed, 1)
        await ed.shot(str(IMG / "06-notify-ts.png"))
        await asyncio.sleep(1.5)
        br.dt = None
        await br.load()
        await br.devtools()
        await add(br, "Не открывается журнал", "212", "Интернет")
        await br.page.wait_for_timeout(1500)
        await br.shot(IMG / "07-ne-otpravleno.png", console=True)
        await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name == "reset":
        reset()
    elif name == "all":
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: reset, all")
