"""Кадры главы 1.6: формы и отправка данных.

Продолжает проект zayavki после главы 1.5. Код — из tools/code16. Браузер и консоль —
как в tools/shots_15.py (headless Chromium с портом 9471).

    python3 tools/shots_16.py reset   # проект в состоянии конца главы 1.5
    python3 tools/shots_16.py all
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
from shots_13 import go_line  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/16-formy/img/raw"
C15 = Path(__file__).parent / "code15"
CODE = Path(__file__).parent / "code16"
SRC = s11.PROJECT / "src"


def reset() -> None:
    """Состояние конца главы 1.5."""
    s15.reset()
    for name in ("App.tsx", "index.css", "requests.ts"):
        shutil.copy(C15 / name, SRC / name)
    shutil.copy(C15 / "RequestCard.tsx", SRC / "components/RequestCard.tsx")
    print("проект в состоянии конца главы 1.5")


def put(src_name: str, dest: str) -> None:
    shutil.copy(CODE / src_name, SRC / dest)


async def fill(br: s15.Browser, title: str, room: str, category: str, details: str) -> None:
    page = br.page
    await page.locator("#title").press_sequentially(title, delay=20)
    await page.locator("#room").press_sequentially(room, delay=20)
    await page.locator("#category").select_option(category)
    await page.locator("#details").press_sequentially(details, delay=10)
    await page.wait_for_timeout(300)


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

        # §2. Поле с value без onChange: текст не набирается, React предупреждает.
        put("requests.ts", "requests.ts")
        put("RequestCard.tsx", "components/RequestCard.tsx")
        put("App-category.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/requests.ts")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "00a-requests-category.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.full(IMG / "00b-kategorii.png")
        put("RequestForm-value.tsx", "components/RequestForm.tsx")
        await asyncio.sleep(1.5)
        await br.load()
        await br.devtools()
        await br.load()
        await br.page.locator("#title").press_sequentially("Проектор", delay=30)
        await br.shot(IMG / "01-value-bez-onchange.png", console=True)

        # Управляемая форма: строка под полями показывает состояние.
        put("RequestForm-controlled.tsx", "components/RequestForm.tsx")
        await s14.reveal(ed, "zayavki/src/components/RequestForm.tsx")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "02-controlled-kod.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.full(IMG / "03-controlled-pusto.png")
        await fill(br, "Не печатает принтер", "118", "Принтер", "")
        await br.full(IMG / "04-controlled-nabrano.png")

        # §3. Отправка: новая заявка в начале списка, форма очищена.
        put("RequestForm-submit.tsx", "components/RequestForm.tsx")
        put("App.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 18)
        await ed.shot(str(IMG / "05-app-handleadd.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await fill(br, "Не печатает принтер", "118", "Принтер", "Принтер в коридоре мигает красной лампой.")
        await br.full(IMG / "06-forma-zapolnena.png")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.full(IMG / "07-novaya-zayavka.png")

        # Пустая заявка без проверки.
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.full(IMG / "08-pustaya-zayavka.png")

        # §4. Проверка полей.
        put("index.css", "index.css")
        put("RequestForm.tsx", "components/RequestForm.tsx")
        await s14.reveal(ed, "zayavki/src/components/RequestForm.tsx")
        await go_line(ed, 18)
        await ed.shot(str(IMG / "09-forma-proverka.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.page.locator("#title").press_sequentially("   ", delay=30)
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.full(IMG / "10-oshibka.png")
        await fill(br, "Не открывается сайт колледжа", "305", "Интернет", "")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.full(IMG / "11-posle-oshibki.png")
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
