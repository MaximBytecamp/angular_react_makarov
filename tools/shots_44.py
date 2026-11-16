"""Кадры главы 4.4: страница «Сайты» монитора на Angular 22.

Проект /private/tmp/student/monitoring-ng создаётся командой ng new рядом с monitoring (React).
Помощники (окно VS Code, кадр кода, кадр терминала) — из shots_33.py; браузер — headless Chromium с адресной строкой.

    python3 tools/shots_44.py all
"""
import asyncio
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import addrbar  # noqa: E402
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_33 as s33  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/44-angular/img/raw"
s33.IMG = IMG
# Порт 9361 бывает занят Chrome соседней съёмки (профиль gh41).
cdp.PORT = 9362
CODE = Path(__file__).parent / "code44"
STUDENT = Path("/private/tmp/student")
REACT = STUDENT / "monitoring"
NG = STUDENT / "monitoring-ng"
NEW = "npx @angular/cli@22.2.7 new monitoring-ng --defaults --style=css --ssr=false --ai-config=open-ai-codex"
URL = "http://localhost:4200/"


async def open_editor(folder: Path) -> cdp.Editor:
    cdp.launch(str(folder))
    await asyncio.sleep(6)
    ed = cdp.Editor()
    await ed.__aenter__()
    await ed.size(1240, 780)
    await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
    await ed.palette("View: Close All Editors", 1.0)
    await ed.palette("View: Close Panel", 1.0)
    await ed.palette("View: Show Explorer", 1.0)
    return ed


async def term(ed: cdp.Editor, command: str, name: str, wait: float) -> None:
    await ed.palette("Terminal: Kill All Terminals", 1.5)
    await s11.open_terminal(ed)
    await s11.terminal(ed, command, wait)
    await s33.term(ed, name)
    await ed.palette("View: Close Panel", 1)


def put(name: str, dest: str) -> None:
    (NG / dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(CODE / name, NG / dest)


class Page:
    async def start(self) -> None:
        from playwright.async_api import async_playwright
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch()
        self.page = await self.browser.new_page(viewport={"width": 1100, "height": 700}, device_scale_factor=2)

    async def shot(self, name: str) -> None:
        path = IMG / name
        await self.page.wait_for_timeout(800)
        await self.page.screenshot(path=str(path))
        addrbar.add(path, self.page.url, await self.page.title())
        print(f"  ✓ {path}")

    async def close(self) -> None:
        await self.browser.close()
        await self.pw.stop()


async def stage_all() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(NG, ignore_errors=True)

    # §2. Новый проект.
    ed = await open_editor(STUDENT)
    await term(ed, NEW, "01-ng-new.png", 90)
    await ed.__aexit__(None, None, None)

    ed = await open_editor(NG)
    await s33.code(ed, "src/app/app.ts", 1, "02-app-ts.png")
    await s33.code(ed, "AGENTS.md", 1, "03-agents-md.png")
    await ed.palette("View: Close All Editors", 1.0)

    # §3–5. Перенос: общие функции, данные, служба, страница, маршруты.
    for f in ("types.ts", "status.ts", "plural.ts"):
        shutil.copy(REACT / "src" / f, NG / "src/app" / f)
    (NG / "public/data").mkdir(parents=True, exist_ok=True)
    for f in ("sites.json", "results.json"):
        shutil.copy(REACT / "public/data" / f, NG / "public/data" / f)
    styles = (REACT / "src/index.css").read_text() + "".join((Path(__file__).parent / "code43/index.css").read_text().splitlines(True)[-2:])
    (NG / "src/styles.css").write_text(styles)
    for f in ("app.html", "app.css", "app.spec.ts"):
        (NG / "src/app" / f).unlink(missing_ok=True)
    put("monitoring.ts", "src/app/monitoring.ts")
    put("sites-page.ts", "src/app/pages/sites-page.ts")
    put("sites-page.html", "src/app/pages/sites-page.html")
    put("site-page.ts", "src/app/pages/site-page.ts")
    put("app.routes.ts", "src/app/app.routes.ts")
    put("app.config.ts", "src/app/app.config.ts")
    put("app.ts", "src/app/app.ts")
    await s33.code(ed, "src/app/monitoring.ts", 1, "04-monitoring-ts.png")
    await s33.code(ed, "src/app/pages/sites-page.ts", 1, "05-sites-page-ts.png")
    await s33.code(ed, "src/app/pages/sites-page.html", 1, "06-sites-page-html.png")
    await s33.code(ed, "src/app/app.routes.ts", 1, "07-app-routes.png")
    await s33.code(ed, "src/app/app.config.ts", 1, "08-app-config.png")
    await ed.palette("View: Close All Editors", 1.0)

    # Запуск и проверка в браузере.
    await ed.palette("Terminal: Kill All Terminals", 1.5)
    await s11.open_terminal(ed)
    await s11.terminal(ed, "npm start", 12)
    await s33.term(ed, "09-ng-serve.png")
    await ed.palette("View: Close Panel", 1)
    for _ in range(60):
        try:
            urllib.request.urlopen(URL)
            break
        except OSError:
            await asyncio.sleep(1)
    br = Page()
    await br.start()
    await br.page.goto(URL)
    await br.page.wait_for_timeout(2500)
    await br.shot("10-sajty.png")
    await br.page.get_by_label("Поиск по названию").fill("справ")
    await br.shot("11-poisk.png")
    await br.page.get_by_label("Поиск по названию").fill("")
    await br.page.locator("a.site").last.click()
    await br.page.wait_for_timeout(1000)
    await br.shot("12-sajt.png")
    await br.close()
    await ed.palette("Terminal: Kill All Terminals", 1.5)

    # §6. Тест и сборка.
    put("sites-page.spec.ts", "src/app/pages/sites-page.spec.ts")
    await s33.code(ed, "src/app/pages/sites-page.spec.ts", 28, "13-spec.png")
    await ed.palette("View: Close All Editors", 1.0)
    await term(ed, "CI=true npm test", "14-ng-test.png", 20)
    await term(ed, "npm run build", "15-ng-build.png", 15)
    await ed.__aexit__(None, None, None)


if __name__ == "__main__":
    asyncio.run({"all": stage_all}[sys.argv[1]]())
