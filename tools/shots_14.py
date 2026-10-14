"""Кадры главы 1.4: состояние и события.

Продолжает проект zayavki после главы 1.3 (tools/shots_13.py all). Код — из tools/code14.
Консоль браузера снимается в фоне: headless Chromium запускается с портом отладки,
а DevTools открывается в нём же отдельной страницей (inspector.html?ws=…).
Порт 9471: 9333 занят другим Chrome пользователя.

    python3 tools/shots_14.py reset   # проект в состоянии конца главы 1.3
    python3 tools/shots_14.py all
"""
import asyncio
import json
import shutil
import sys
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
from shots_13 import go_line  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/14-sostoyanie-i-sobytiya/img/raw"
C12 = Path(__file__).parent / "code12"
C13 = Path(__file__).parent / "code13"
CODE = Path(__file__).parent / "code14"
SRC = s11.PROJECT / "src"
PORT = 9471
URL = "http://localhost:5173/"


def reset() -> None:
    """Состояние конца главы 1.3."""
    shutil.copy(C12 / "Header.tsx", SRC / "components/Header.tsx")
    shutil.copy(C12 / "RequestForm.tsx", SRC / "components/RequestForm.tsx")
    shutil.copy(C13 / "RequestCard.tsx", SRC / "components/RequestCard.tsx")
    shutil.copy(C13 / "App.tsx", SRC / "App.tsx")
    shutil.copy(C12 / "index.css", SRC / "index.css")
    print("проект в состоянии конца главы 1.3")


def put(src_name: str, dest: str) -> None:
    shutil.copy(CODE / src_name, SRC / dest)


class Browser:
    """Страница доски и (по желанию) DevTools с открытой вкладкой Console."""

    async def start(self) -> None:
        from playwright.async_api import async_playwright
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(
            channel="chromium", args=[f"--remote-debugging-port={PORT}", "--remote-allow-origins=*"])
        self.ctx = await self.browser.new_context(viewport={"width": 1100, "height": 700}, device_scale_factor=2)
        self.page = await self.ctx.new_page()
        self.errors: list[str] = []
        self.page.on("pageerror", lambda e: self.errors.append(str(e)))
        self.dt = None

    async def load(self) -> None:
        await self.page.goto(URL)
        await self.page.wait_for_timeout(1500)

    async def devtools(self) -> None:
        """Открывает DevTools для страницы доски и очищает консоль."""
        if self.dt is None:
            targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json").read())
            tid = next(t["id"] for t in targets if t["url"].startswith(URL))
            self.dt = await self.ctx.new_page()
            # Удалённый DevTools показывает слева трансляцию страницы; настройка её выключает.
            await self.dt.add_init_script("localStorage.setItem('screencast-enabled', 'false')")
            await self.dt.set_viewport_size({"width": 1100, "height": 250})
            await self.dt.goto(f"http://127.0.0.1:{PORT}/devtools/inspector.html?ws=127.0.0.1:{PORT}/devtools/page/{tid}")
            await self.dt.wait_for_timeout(3000)
            try:
                await self.dt.get_by_text("Don't show again").click(timeout=2000)
            except Exception:
                pass
            await self.dt.get_by_role("tab", name="Console").click()
            await self.dt.wait_for_timeout(800)
        await self.dt.locator('[aria-label="Clear console"]').first.click()
        await self.dt.wait_for_timeout(500)

    async def click(self, text: str, nth: int) -> None:
        await self.page.locator("button", has_text=text).nth(nth).click()
        await self.page.wait_for_timeout(400)

    async def shot(self, path: Path, console: bool = False) -> None:
        """Страница; с console=True под ней панель Console, как DevTools, пристыкованный снизу."""
        await self.page.wait_for_timeout(800)
        await self.page.screenshot(path=str(path))
        if console:
            await self.dt.wait_for_timeout(800)
            tmp = path.with_suffix(".dt.png")
            await self.dt.screenshot(path=str(tmp))
            top, bottom = Image.open(path), Image.open(tmp)
            top = top.crop((0, 0, top.width, int(top.height * 0.74)))
            out = Image.new("RGB", (top.width, top.height + 4 + bottom.height), "#c4c7cf")
            out.paste(top, (0, 0))
            out.paste(bottom, (0, top.height + 4))
            out.save(path)
            tmp.unlink()
        print(f"  ✓ {path}")

    async def close(self) -> None:
        await self.browser.close()
        await self.pw.stop()


async def reveal(ed: cdp.Editor, rel: str) -> None:
    await s11.open_file(ed, rel)
    await ed.palette("File: Revert File", 1.0)


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
        br = Browser()
        await br.start()

        # §1. Кнопка и обработчик: сообщения в консоли.
        put("index-knopka.css", "index.css")
        put("RequestCard-click.tsx", "components/RequestCard.tsx")
        await reveal(ed, "zayavki/src/components/RequestCard.tsx")
        await ed.shot(str(IMG / "01-knopka-obrabotchik.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.devtools()
        for i in range(3):
            await br.click("Взять в работу", i)
        await br.shot(IMG / "02-konsol-nazhatiya.png", console=True)

        # §2. Обычная переменная: в консоли новое значение, на странице старое.
        put("RequestCard-let.tsx", "components/RequestCard.tsx")
        await asyncio.sleep(2)
        await br.load()
        await br.devtools()
        await br.click("Взять в работу", 0)
        await br.click("Взять в работу", 0)
        await br.shot(IMG / "03-peremennaya-let.png", console=True)

        # Линтер находит присваивание после отрисовки.
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki && npm run lint", 5)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "04-lint-let.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
        await ed.palette("Terminal: Kill the Active Terminal Instance", 1.0)
        await ed.palette("View: Close Panel", 1)

        # §3. useState.
        put("RequestCard-state.tsx", "components/RequestCard.tsx")
        await reveal(ed, "zayavki/src/components/RequestCard.tsx")
        await ed.shot(str(IMG / "05-usestate.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.click("Взять в работу", 0)
        await br.click("Завершить", 1)
        await br.shot(IMG / "06-sostoyanie-kartochek.png")

        # Ошибка: вызов обработчика вместо передачи.
        bad = (CODE / "RequestCard-state.tsx").read_text().replace(
            "onClick={handleClick}", "onClick={handleClick()}")
        (SRC / "components/RequestCard.tsx").write_text(bad)
        await asyncio.sleep(2)
        br.errors.clear()
        await br.devtools()
        await br.load()
        await br.shot(IMG / "07-vyzov-vmesto-peredachi.png", console=True)
        print("  ошибки страницы:", br.errors[:1])

        # §5. Состояние в App, счётчик в шапке.
        put("index.css", "index.css")
        put("RequestCard.tsx", "components/RequestCard.tsx")
        put("Header.tsx", "components/Header.tsx")
        put("App.tsx", "App.tsx")
        await reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "08-app-sostoyanie.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.shot(IMG / "09-schetchik-1.png")
        await br.click("Взять в работу", 0)
        await br.shot(IMG / "10-schetchik-0.png")
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
