"""Кадры главы 3.1: маршрутизация на доске заявок.

Продолжает проект zayavki после главы 2.5 (код code24/code25) и PocketBase с заявками конца модуля 2
(code31/db-start.json). Перед съёмкой проект и база приводятся к этому состоянию, react-router удаляется.
Над кадрами браузера дорисовывается адресная строка (addrbar.py).

    python3 tools/shots_31.py all
"""
import asyncio
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import addrbar  # noqa: E402
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_14 as s14  # noqa: E402
import shots_15 as s15  # noqa: E402
import shots_23 as s23  # noqa: E402
from shots_13 import go_line  # noqa: E402
from shots_22 import EMAIL, PASSWORD  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/31-marshrutizaciya/img/raw"
TOOLS = Path(__file__).parent
CODE = TOOLS / "code31"
SRC = s11.PROJECT / "src"
BASE = "http://localhost:5173"
MAIN = """import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
"""
SCREEN = "Не показывает экран на стене"


def reset_db() -> None:
    """Заявки конца модуля 2: лишние удаляются, статус и категория возвращаются, недостающие создаются."""
    token = s23.api("POST", "/api/collections/_superusers/auth-with-password",
                    body={"identity": EMAIL, "password": PASSWORD})["token"]
    path = "/api/collections/requests/records"
    start = {r["title"]: r for r in json.loads((CODE / "db-start.json").read_text())}
    items = s23.api("GET", f"{path}?perPage=200", token)["items"]
    for item in items:
        want = start.get(item["title"])
        if want is None:
            s23.api("DELETE", f"{path}/{item['id']}", token)
        elif (item["status"], item["category"]) != (want["status"], want["category"]):
            s23.api("PATCH", f"{path}/{item['id']}", token, {"status": want["status"], "category": want["category"]})
    have = {i["title"] for i in items}
    for title, want in start.items():
        if title not in have:
            s23.api("POST", path, token, want)


def reset() -> None:
    """Проект конца главы 2.5 без react-router."""
    for name, src in (("App.tsx", "code24/App.tsx"), ("useRequests.ts", "code25/useRequests.ts"),
                      ("requests.ts", "code25/requests.ts"), ("realtime.ts", "code25/realtime.ts"),
                      ("api.ts", "code23/api.ts"), ("index.css", "code23/index.css"),
                      ("components/Header.tsx", "code14/Header.tsx"),
                      ("components/RequestCard.tsx", "code16/RequestCard.tsx")):
        shutil.copy(TOOLS / src, SRC / name)
    (SRC / "main.tsx").write_text(MAIN)
    shutil.rmtree(SRC / "pages", ignore_errors=True)
    for name in ("package.json", "package-lock.json"):
        shutil.copy(TOOLS / "code25" / name, s11.PROJECT / name)
    subprocess.run(["npm", "ci", "--prefer-offline"], cwd=s11.PROJECT, capture_output=True,
                   env={"PATH": f"{cdp.NODE_BIN}:/usr/bin:/bin", "HOME": str(Path.home()),
                        "npm_config_cache": "/private/tmp/student/npm-cache"})


def put(name: str, dest: str) -> None:
    (SRC / dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(CODE / name, SRC / dest)


async def code(ed: cdp.Editor, rel: str, line: int, name: str) -> None:
    await s14.reveal(ed, f"zayavki/src/{rel}")
    await ed.palette("File: Reveal Active File in Explorer View", 1.0)
    await go_line(ed, line)
    await ed.shot(str(IMG / name))


async def go(br: s15.Browser, path: str) -> None:
    await br.page.goto(BASE + path)
    await br.page.wait_for_timeout(1500)


async def page(br: s15.Browser, name: str, console: bool = False) -> None:
    """Окно браузера 1100×900 с адресной строкой сверху."""
    await br.shot(IMG / name, console=console)
    addrbar.add(IMG / name, br.page.url)


async def network(br: s15.Browser) -> None:
    """Вкладка Network со всеми типами запросов."""
    await br.devtools()
    await br.dt.set_viewport_size({"width": 1100, "height": 400})
    await br.dt.get_by_role("tab", name="Network").click()
    await br.dt.wait_for_timeout(800)
    await br.dt.get_by_text("All", exact=True).first.click()
    await br.dt.wait_for_timeout(400)


async def clear_network(br: s15.Browser) -> None:
    await br.dt.locator('[aria-label="Clear network log"]').first.click()
    await br.dt.wait_for_timeout(400)


async def all_frames() -> None:
    reset()
    reset_db()
    cdp.launch(str(s11.WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1240, 780)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await asyncio.sleep(3)
        await ed.palette("View: Close All Editors", 1.0)
        await ed.palette("View: Collapse Folders in Explorer", 1.0)
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki && npm run dev", 6)
        await ed.palette("View: Close Panel", 1)
        await ed.palette("View: Show Explorer", 1.2)
        br = s15.Browser()
        await br.start()
        await asyncio.sleep(1.5)

        # §1. Адрес /stats до маршрутизации: та же доска.
        await go(br, "/stats")
        await page(br, "01-stats-do.png")

        # §2. Библиотека и два маршрута.
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki", 1)
        await s11.terminal(ed, "npm install react-router@8.5.1", 12)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "02-npm-install.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
        await ed.palette("View: Close Panel", 1)
        put("main.tsx", "main.tsx")
        await code(ed, "main.tsx", 1, "03-main.png")
        put("BoardPage-2.tsx", "pages/BoardPage.tsx")
        await code(ed, "pages/BoardPage.tsx", 20, "04-boardpage.png")
        put("StatsPage.tsx", "pages/StatsPage.tsx")
        await code(ed, "pages/StatsPage.tsx", 1, "05-statspage.png")
        put("index.css", "index.css")
        await code(ed, "index.css", 250, "05a-index-css.png")
        put("App-routes.tsx", "App.tsx")
        await code(ed, "App.tsx", 84, "06-app-routes.png")
        await asyncio.sleep(2)
        await go(br, "/")
        await page(br, "07-glavnaya.png")
        await go(br, "/stats")
        await page(br, "08-stats.png")
        await br.devtools()
        await go(br, "/abc")
        await page(br, "09-abc-pusto.png", console=True)
        put("NotFoundPage.tsx", "pages/NotFoundPage.tsx")
        await code(ed, "pages/NotFoundPage.tsx", 1, "10-notfound-code.png")
        put("App-notfound.tsx", "App.tsx")
        await code(ed, "App.tsx", 86, "11-app-notfound.png")
        await asyncio.sleep(1.5)
        await go(br, "/abc")
        await page(br, "12-notfound.png")

        # §3. Ссылка <a href> перезагружает страницу, NavLink — нет.
        put("Header-a.tsx", "components/Header.tsx")
        await code(ed, "components/Header.tsx", 1, "13-header-a.png")
        await asyncio.sleep(1.5)
        await network(br)
        await go(br, "/")
        await clear_network(br)
        await br.page.locator(".nav a", has_text="Статистика").click()
        await br.page.wait_for_timeout(2000)
        await page(br, "14-a-network.png", console=True)
        put("Header.tsx", "components/Header.tsx")
        await code(ed, "components/Header.tsx", 1, "15-header-navlink.png")
        await asyncio.sleep(1.5)
        await go(br, "/")
        await clear_network(br)
        await br.page.locator(".nav a", has_text="Статистика").click()
        await br.page.wait_for_timeout(2000)
        await page(br, "16-navlink-network.png", console=True)
        await br.dt.close()
        br.dt = None
        await go(br, "/")
        await br.page.locator(".filters button", has_text="Новая").click()
        await page(br, "17-filtr-novaya.png")
        await br.page.locator(".nav a", has_text="Статистика").click()
        await br.page.wait_for_timeout(800)
        await br.page.locator(".nav a", has_text="Заявки").click()
        await page(br, "18-filtr-sbros.png")

        # §4. Страница заявки по адресу /requests/:id.
        put("RequestCard.tsx", "components/RequestCard.tsx")
        await code(ed, "components/RequestCard.tsx", 26, "19-requestcard.png")
        put("BoardPage.tsx", "pages/BoardPage.tsx")
        await code(ed, "pages/BoardPage.tsx", 57, "20-boardpage-id.png")
        put("RequestPage.tsx", "pages/RequestPage.tsx")
        await code(ed, "pages/RequestPage.tsx", 20, "21-requestpage.png")
        put("App.tsx", "App.tsx")
        await code(ed, "App.tsx", 86, "22-app-route.png")
        await asyncio.sleep(1.5)
        await go(br, "/")
        await br.page.locator(".card h3 a", has_text=SCREEN).click()
        await br.page.wait_for_timeout(1000)
        await page(br, "23-zayavka.png")
        await br.page.reload()
        await br.page.wait_for_timeout(1500)
        await go(br, "/requests/abc")
        await page(br, "24-net-zayavki.png")
        await br.page.go_back()
        await br.page.wait_for_timeout(1500)
        await br.page.get_by_role("button", name="Завершить").click()
        await br.page.wait_for_timeout(1200)
        await page(br, "25-zavershena.png")
        await br.page.get_by_role("button", name="Убрать с доски").click()
        await br.page.wait_for_timeout(1500)
        await page(br, "26-ubrana.png")
        await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: all")
