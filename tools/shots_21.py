"""Кадры главы 2.1: эффекты и когда они не нужны.

Продолжает проект zayavki после главы 1.7. Код — из tools/code21. Консоль браузера —
как в tools/shots_14.py (headless Chromium с портом 9471). Заголовок вкладки в headless-браузере
не виден, поэтому он показан ответом консоли на выражение document.title.

    python3 tools/shots_21.py all
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
IMG = ROOT / "temy/21-effekty/img/raw"
C17 = Path(__file__).parent / "code17"
CODE = Path(__file__).parent / "code21"
SRC = s11.PROJECT / "src"


def reset() -> None:
    """Состояние конца главы 1.7."""
    for name in ("App.tsx", "index.css", "requests.ts", "storage.ts", "notify.ts"):
        shutil.copy(C17 / name, SRC / name)
    for name in ("RequestCard.tsx", "RequestForm.tsx"):
        shutil.copy(C17 / name, SRC / "components" / name)
    shutil.copy(Path(__file__).parent / "code14/Header.tsx", SRC / "components/Header.tsx")


def put(name: str) -> None:
    shutil.copy(CODE / name, SRC / "App.tsx")


async def fresh(br: s15.Browser) -> None:
    """Чистая доска и пустая консоль."""
    await br.load()
    await br.page.evaluate("localStorage.clear()")
    if br.dt is None:
        await br.devtools()
    else:
        await br.dt.locator('[aria-label="Clear console"]').first.click()
    await br.load()
    await br.page.wait_for_timeout(800)


async def console_eval(br: s15.Browser, expr: str) -> None:
    prompt = br.dt.locator(".console-prompt-editor-container").first
    await prompt.click()
    await br.dt.keyboard.type(expr)
    await br.dt.keyboard.press("Enter")
    await br.dt.wait_for_timeout(600)


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
        await asyncio.sleep(1.5)
        await br.load()

        # §2. Эффект с заголовком: код и журнал запусков.
        put("App-title.tsx")
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 14)
        await ed.shot(str(IMG / "01-app-title.png"))

        put("App-title-log.tsx")
        await asyncio.sleep(1.5)
        await fresh(br)
        await br.shot(IMG / "02-log-zagruzka.png", console=True)
        await br.page.locator(".filters button", has_text="Новая").click()
        await br.page.wait_for_timeout(500)
        await br.shot(IMG / "03-log-filtr.png", console=True)
        await br.page.locator(".filters button", has_text="Все").click()
        await br.click("Взять в работу", 0)
        await br.page.wait_for_timeout(500)
        await br.shot(IMG / "04-log-status.png", console=True)
        await br.dt.locator('[aria-label="Clear console"]').first.click()
        await console_eval(br, "document.title")
        await br.shot(IMG / "05-title.png", console=True)

        put("App-title-log-bez-massiva.tsx")
        await asyncio.sleep(1.5)
        await fresh(br)
        await br.dt.locator('[aria-label="Clear console"]').first.click()
        await br.page.locator(".filters button", has_text="Новая").click()
        await br.page.locator(".filters button", has_text="Готово").click()
        await br.page.wait_for_timeout(500)
        await br.shot(IMG / "06-bez-massiva.png", console=True)

        # Пропущенная зависимость: линтер и застывший заголовок.
        put("App-title-bez-zavisimosti.tsx")
        await asyncio.sleep(1.5)
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki && npm run lint", 5)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "07-lint-deps.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
        await fresh(br)
        await br.click("Взять в работу", 0)
        await br.dt.locator('[aria-label="Clear console"]').first.click()
        await console_eval(br, "document.title")
        await br.shot(IMG / "08-title-zastyl.png", console=True)

        # §3. Таймер сообщения.
        put("App-notice.tsx")
        await asyncio.sleep(1.5)
        await fresh(br)
        await s16.fill(br, "Не работает звонок", "Вахта", "Компьютер", "")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.page.wait_for_timeout(1500)
        await br.shot(IMG / "09-soobshchenie.png")
        await br.page.wait_for_timeout(5500)
        await br.shot(IMG / "10-soobshchenie-skrylos.png")

        # §4. Клавиша Esc: без очистки и с очисткой.
        put("App-esc-bez-ochistki.tsx")
        await asyncio.sleep(1.5)
        await fresh(br)
        await br.dt.locator('[aria-label="Clear console"]').first.click()
        await br.page.locator(".filters button", has_text="Готово").click()
        await br.page.mouse.click(1000, 120)
        await br.page.keyboard.press("Escape")
        await br.page.wait_for_timeout(600)
        await br.shot(IMG / "11-esc-bez-ochistki.png", console=True)

        put("App.tsx")
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 33)
        await ed.shot(str(IMG / "12-app-effekty.png"))
        await asyncio.sleep(1.5)
        await fresh(br)
        await br.page.locator(".filters button", has_text="Готово").click()
        await br.page.wait_for_timeout(400)
        await br.full(IMG / "13-filtr-gotovo.png")
        await br.page.mouse.click(1000, 120)
        await br.page.keyboard.press("Escape")
        await br.page.wait_for_timeout(600)
        await br.full(IMG / "14-esc-vse.png")

        # §5. Эффект там, где он не нужен.
        put("App-visible-effekt.tsx")
        await asyncio.sleep(1.5)
        await s11.terminal(ed, "npm run lint", 5)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "15-lint-set-state.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
        await fresh(br)
        await br.dt.locator('[aria-label="Clear console"]').first.click()
        await br.page.locator(".filters button", has_text="Новая").click()
        await br.page.wait_for_timeout(600)
        await br.shot(IMG / "16-lishnyaya-otrisovka.png", console=True)

        put("App.tsx")
        await asyncio.sleep(1.0)
        await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: all")
