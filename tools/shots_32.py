"""Кадры главы 3.2: контекст с данными доски.

Продолжает проект zayavki после главы 3.1 (code31) и PocketBase с заявками конца главы 3.1
(code32/db-start.json). Над кадрами браузера дорисовывается адресная строка (addrbar.py).

    python3 tools/shots_32.py all
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
IMG = ROOT / "temy/32-kontekst/img/raw"
TOOLS = Path(__file__).parent
C31 = TOOLS / "code31"
CODE = TOOLS / "code32"
SRC = s11.PROJECT / "src"
BASE = "http://localhost:5173"
BOARD = "Не работает интерактивная доска"


def reset_db() -> None:
    """Заявки конца главы 3.1: лишние удаляются, статус и категория возвращаются, недостающие создаются."""
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
    """Проект конца главы 3.1."""
    for name in ("main.tsx", "App.tsx", "index.css"):
        shutil.copy(C31 / name, SRC / name)
    for name in ("Header.tsx", "RequestCard.tsx"):
        shutil.copy(C31 / name, SRC / "components" / name)
    (SRC / "pages").mkdir(exist_ok=True)
    for name in ("BoardPage.tsx", "StatsPage.tsx", "RequestPage.tsx", "NotFoundPage.tsx"):
        shutil.copy(C31 / name, SRC / "pages" / name)
    for name in ("board.ts", "BoardProvider.tsx"):
        (SRC / name).unlink(missing_ok=True)
    for name in ("package.json", "package-lock.json"):
        shutil.copy(C31 / name, s11.PROJECT / name)
    subprocess.run(["npm", "ci", "--prefer-offline"], cwd=s11.PROJECT, capture_output=True,
                   env={"PATH": f"{cdp.NODE_BIN}:/usr/bin:/bin", "HOME": str(Path.home()),
                        "npm_config_cache": "/private/tmp/student/npm-cache"})


def put(name: str, dest: str) -> None:
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
    await br.shot(IMG / name, console=console)
    addrbar.add(IMG / name, br.page.url)


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
        await go(br, "/")

        # §2. Контекст, провайдер, App читает useBoard; сначала без провайдера.
        put("board.ts", "board.ts")
        await code(ed, "board.ts", 1, "01-board-ts.png")
        put("BoardProvider.tsx", "BoardProvider.tsx")
        await code(ed, "BoardProvider.tsx", 60, "02-provider.png")
        put("App-context.tsx", "App.tsx")
        await code(ed, "App.tsx", 1, "03-app-context.png")
        await asyncio.sleep(1.5)
        await br.devtools()
        await go(br, "/")
        await page(br, "04-bez-providera.png", console=True)
        put("main.tsx", "main.tsx")
        await code(ed, "main.tsx", 1, "05-main.png")
        await asyncio.sleep(1.5)
        await br.dt.locator('[aria-label="Clear console"]').first.click()
        await go(br, "/")
        await page(br, "06-doska.png", console=True)

        # §3. Страницы берут данные из контекста, App — только маршруты.
        put("StatsPage.tsx", "pages/StatsPage.tsx")
        await code(ed, "pages/StatsPage.tsx", 1, "07-statspage.png")
        put("RequestPage.tsx", "pages/RequestPage.tsx")
        await code(ed, "pages/RequestPage.tsx", 1, "08-requestpage.png")
        put("BoardPage.tsx", "pages/BoardPage.tsx")
        await code(ed, "pages/BoardPage.tsx", 13, "09-boardpage.png")
        put("Header.tsx", "components/Header.tsx")
        await code(ed, "components/Header.tsx", 1, "10-header.png")
        put("App.tsx", "App.tsx")
        await code(ed, "App.tsx", 1, "11-app.png")
        await asyncio.sleep(1.5)
        await s23.network_tab(br)
        await go(br, "/")
        await page(br, "12-network.png", console=True)
        await br.dt.close()
        br.dt = None

        # §4. Шапка, страница заявки и статистика читают один список.
        await go(br, "/")
        await br.page.locator(".card h3 a", has_text=BOARD).click()
        await br.page.wait_for_timeout(1000)
        await page(br, "13-zayavka.png")
        await br.page.get_by_role("button", name="Взять в работу").click()
        await br.page.wait_for_timeout(1200)
        await page(br, "14-vzyata.png")
        await br.page.locator(".nav a", has_text="Статистика").click()
        await br.page.wait_for_timeout(800)
        await page(br, "15-stats.png")
        await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: all")
