"""Кадры главы 4.2: доступность приложения «Мониторинг сайтов группы».

Продолжает проект /private/tmp/student/monitoring после главы 4.1.
Помощники (окно VS Code, кадр кода, кадр терминала, браузер с адресной строкой) — из shots_33.py.
DevTools открывается отдельной вкладкой по протоколу отладки; Lighthouse запускается в его панели.
Этапы те же, что проверяет tools/verify_42.sh.

    python3 tools/shots_42.py all
"""
import asyncio
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import addrbar  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_33 as s33  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/42-dostupnost/img/raw"
s33.IMG = IMG
# Порт 9361 бывает занят Chrome соседней съёмки (профиль gh41).
s33.cdp.PORT = 9362
CODE = Path(__file__).parent / "code42"
C41 = Path(__file__).parent / "code41"
P3 = Path(__file__).parent / "proekt3-monitoring/src"
PROJECT = s33.PROJECT
URL = "http://localhost:5173/monitoring/"
DEBUG = 9472


def put(name: str, dest: str, src: Path = CODE) -> None:
    shutil.copy(src / name, PROJECT / dest)


def reset() -> None:
    """Проект в состоянии после главы 4.1."""
    shutil.copy(P3 / "index.css", PROJECT / "src/index.css")
    for f in ("SitePage", "AboutPage", "NotFoundPage"):
        shutil.copy(P3 / f"pages/{f}.tsx", PROJECT / f"src/pages/{f}.tsx")
    put("SitesPage.tsx", "src/pages/SitesPage.tsx", C41)
    put("SitesPage.test.tsx", "src/pages/SitesPage.test.tsx", C41)
    put("App.test.tsx", "src/App.test.tsx", C41)
    put("MonitoringProvider.test.tsx", "src/MonitoringProvider.test.tsx", C41)
    put("deploy.yml", ".github/workflows/deploy.yml", C41)
    subprocess.run(["git", "checkout", "--", ".oxlintrc.json", "public/data/results.json"], cwd=PROJECT, check=True)


def dev_server() -> subprocess.Popen:
    env = {"PATH": f"{s33.cdp.NODE_BIN}:/usr/bin:/bin"}
    proc = subprocess.Popen([f"{s33.cdp.NODE_BIN}/npx", "vite", "--port", "5173", "--strictPort"], cwd=PROJECT,
                            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        try:
            urllib.request.urlopen(URL)
            return proc
        except OSError:
            import time
            time.sleep(0.5)
    raise SystemExit("vite не запустился")


class Browser:
    """Headless Chromium 1100×700 и DevTools этой страницы в соседней вкладке."""

    async def start(self) -> None:
        from playwright.async_api import async_playwright
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(
            channel="chromium", args=[f"--remote-debugging-port={DEBUG}", "--remote-allow-origins=*"])
        self.ctx = await self.browser.new_context(viewport={"width": 1100, "height": 700}, device_scale_factor=2)
        self.page = await self.ctx.new_page()
        self.dt = None

    async def go(self, path: str = "") -> None:
        await self.page.goto(URL + path)
        await self.page.wait_for_timeout(2000)

    async def shot(self, name: str, title: bool = False) -> None:
        path = IMG / name
        await self.page.wait_for_timeout(800)
        await self.page.screenshot(path=str(path))
        addrbar.add(path, self.page.url, await self.page.title() if title else None)
        print(f"  ✓ {path}")

    async def tabs(self, n: int) -> None:
        await self.page.bring_to_front()
        await self.page.mouse.click(5, 690)
        for _ in range(n):
            await self.page.keyboard.press("Tab")
            await self.page.wait_for_timeout(250)

    async def devtools(self, height: int = 700) -> None:
        if self.dt is not None:
            await self.dt.close()
        targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{DEBUG}/json").read())
        tid = next(t["id"] for t in targets if t["type"] == "page" and t["url"].startswith(URL))
        self.dt = await self.ctx.new_page()
        await self.dt.add_init_script("localStorage.setItem('screencast-enabled', 'false')")
        await self.dt.set_viewport_size({"width": 1100, "height": height})
        await self.dt.goto(f"http://127.0.0.1:{DEBUG}/devtools/inspector.html?ws=127.0.0.1:{DEBUG}/devtools/page/{tid}")
        await self.dt.wait_for_timeout(3000)
        try:
            await self.dt.get_by_text("Don't show again").click(timeout=2000)
        except Exception:
            pass

    async def dt_shot(self, name: str) -> None:
        await self.dt.wait_for_timeout(800)
        await self.dt.screenshot(path=str(IMG / name))
        print(f"  ✓ {IMG / name}")

    async def lighthouse(self, panel_shot: str = "") -> None:
        """Панель Lighthouse: только Accessibility, Desktop; отчёт открывается в той же панели."""
        dt = self.dt
        await dt.get_by_role("tab", name="Lighthouse").click()
        await dt.wait_for_timeout(1500)
        for name in ("Performance", "Best practices", "SEO"):
            await dt.get_by_role("checkbox", name=name).uncheck()
        await dt.get_by_role("radio", name="Desktop").check()
        if panel_shot:
            await self.dt_shot(panel_shot)
        await dt.get_by_role("button", name="Analyze page load").click()
        await dt.locator(".lh-gauge__percentage").first.wait_for(timeout=120000)
        await dt.wait_for_timeout(2500)

    async def expand(self, text: str) -> None:
        """Раскрывает проверку отчёта и прокручивает к ней."""
        item = self.dt.get_by_text(text, exact=False).first
        await item.scroll_into_view_if_needed()
        await item.click()
        await self.dt.wait_for_timeout(1000)
        await item.evaluate("e => e.closest('.lh-audit').scrollIntoView({block: 'start'})")
        await self.dt.wait_for_timeout(800)

    async def a11y_pane(self, selector: str) -> None:
        """Элемент выбирается командой inspect() в консоли DevTools, справа — вкладка Accessibility."""
        dt = self.dt
        await dt.get_by_role("tab", name="Console").click()
        await dt.wait_for_timeout(1000)
        await dt.keyboard.type(f"inspect(document.querySelector('{selector}'))")
        await dt.keyboard.press("Enter")
        await dt.wait_for_timeout(1500)
        tab = dt.get_by_role("tab", name="Accessibility")
        if not await tab.is_visible():
            await dt.get_by_role("button", name="More tabs").last.click()
            await dt.wait_for_timeout(800)
            tab = dt.get_by_role("menuitem", name="Accessibility")
        await tab.click()
        await dt.wait_for_timeout(1500)

    async def close(self) -> None:
        await self.browser.close()
        await self.pw.stop()


async def watch_shot(ed, name: str, wait: float = 4.0) -> None:
    await asyncio.sleep(wait)
    await s33.term(ed, name)


async def run(ed, command: str, wait: float) -> None:
    """Команда в новом терминале: прежние закрываются, фокус гарантированно в терминале."""
    await ed.palette("Terminal: Kill All Terminals", 1.5)
    await s11.open_terminal(ed)
    await s11.terminal(ed, command, wait)


async def stage_all() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    reset()
    server = dev_server()
    br = Browser()
    await br.start()

    # §2. Lighthouse на странице после главы 4.1.
    await br.go()
    await br.devtools()
    await br.lighthouse("01-lh-panel.png")
    await br.dt_shot("02-lh-94.png")
    await br.expand("Background and foreground colors")
    await br.dt_shot("03-lh-kontrast.png")
    await br.go("site/staryy")
    await br.devtools()
    await br.lighthouse()
    await br.expand("Background and foreground colors")
    await br.dt_shot("04-lh-91.png")

    ed = await s33.editor()
    # §3. Контраст: новые цвета.
    put("index.css", "src/index.css")
    await s33.code(ed, "src/index.css", 1, "05-index-css.png")
    await ed.palette("View: Close All Editors", 1.0)
    await br.go()
    await br.devtools()
    await br.lighthouse()
    await br.dt_shot("06-lh-100.png")

    # §4. Опыт: карточка на div.
    put("SitesPage-div.tsx", "src/pages/SitesPage.tsx")
    await s33.code(ed, "src/pages/SitesPage.tsx", 34, "07-sitespage-div.png")
    await ed.palette("View: Close All Editors", 1.0)
    await br.go()
    await br.tabs(3)
    await br.shot("08-tab-div.png")
    await run(ed, "npm test", 6)
    await watch_shot(ed, "09-tests-div.png", 2)
    await ed.palette("View: Close Panel", 1)
    put("oxlintrc.json", ".oxlintrc.json")
    await s33.code(ed, ".oxlintrc.json", 1, "10-oxlintrc.png")
    await ed.palette("View: Close All Editors", 1.0)
    await run(ed, "npm run lint", 3)
    await s33.term(ed, "11-lint-div.png")
    await ed.palette("View: Close Panel", 1)
    put("SitesPage.tsx", "src/pages/SitesPage.tsx", C41)
    await br.go()
    await br.tabs(3)
    await br.shot("12-tab-link.png")

    # §5. Дерево доступности: имя ссылки и заголовок вкладки.
    await br.devtools()
    await br.a11y_pane("a[href$=\"staryy\"]")
    await br.dt_shot("13-a11y-do.png")
    await run(ed, "npm test", 6)
    await ed.palette("View: Close Panel", 1)
    put("SitesPage-1.test.tsx", "src/pages/SitesPage.test.tsx")
    await ed.palette("View: Toggle Panel Visibility", 1.0)
    await watch_shot(ed, "14-test-name-red.png")
    await ed.palette("View: Close Panel", 1)
    put("SitesPage-2.tsx", "src/pages/SitesPage.tsx")
    await s33.code(ed, "src/pages/SitesPage.tsx", 34, "15-sitespage-order.png")
    await ed.palette("View: Close All Editors", 1.0)
    await br.go()
    await br.devtools()
    await br.a11y_pane("a[href$=\"staryy\"]")
    await br.dt_shot("16-a11y-posle.png")
    await br.go("site/staryy")
    await br.shot("17-title-do.png", title=True)
    put("App.test.tsx", "src/App.test.tsx")
    await ed.palette("View: Toggle Panel Visibility", 1.0)
    await watch_shot(ed, "18-title-red.png")
    await ed.palette("View: Close Panel", 1)
    for f in ("AboutPage.tsx", "NotFoundPage.tsx"):
        put(f, f"src/pages/{f}")
    put("SitesPage-3.tsx", "src/pages/SitesPage.tsx")
    put("SitePage-1.tsx", "src/pages/SitePage.tsx")
    await s33.code(ed, "src/pages/SitePage.tsx", 20, "19-sitepage-title.png")
    await ed.palette("View: Close All Editors", 1.0)
    await br.go("site/staryy")
    await br.shot("20-title-posle.png", title=True)

    # §6. Сообщения о загрузке и ошибке.
    put("SitesPage.test.tsx", "src/pages/SitesPage.test.tsx")
    put("MonitoringProvider.test.tsx", "src/MonitoringProvider.test.tsx")
    await ed.palette("View: Toggle Panel Visibility", 1.0)
    await watch_shot(ed, "21-roles-red.png")
    await ed.palette("View: Close Panel", 1)
    put("SitesPage.tsx", "src/pages/SitesPage.tsx")
    put("SitePage.tsx", "src/pages/SitePage.tsx")
    await s33.code(ed, "src/pages/SitePage.tsx", 1, "22-sitepage.png")
    await ed.palette("View: Close All Editors", 1.0)
    await ed.palette("View: Toggle Panel Visibility", 1.0)
    await watch_shot(ed, "23-vse-zeleno.png")
    await ed.palette("View: Close Panel", 1)

    # §7. Линтер перед публикацией.
    put("deploy.yml", ".github/workflows/deploy.yml")
    await s33.code(ed, ".github/workflows/deploy.yml", 30, "24-deploy-yml.png")
    await ed.palette("View: Close All Editors", 1.0)
    await run(ed, "npm run lint -- --deny-warnings", 3)
    await s33.term(ed, "25-lint-ok.png")
    await ed.__aexit__(None, None, None)
    await br.close()
    server.terminate()


if __name__ == "__main__":
    asyncio.run({"all": stage_all}[sys.argv[1]]())
