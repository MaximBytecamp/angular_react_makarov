"""Кадры главы 2.3: загрузка заявок из PocketBase, состояние загрузки и ошибки.

Продолжает проект zayavki после главы 2.1 и PocketBase после главы 2.2 (пять заявок
в коллекции requests). Код — из tools/code23. Перед съёмкой база приводится к пяти
заявкам со статусом «Новая», чтобы повторный прогон давал те же кадры.

    python3 tools/shots_23.py all
"""
import asyncio
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_14 as s14  # noqa: E402
import shots_15 as s15  # noqa: E402
import shots_16 as s16  # noqa: E402
from shots_13 import go_line  # noqa: E402
from shots_21 import console_eval, reset as reset21  # noqa: E402,F401
from shots_22 import EMAIL, PASSWORD, PB  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/23-zagruzka/img/raw"
CODE = Path(__file__).parent / "code23"
SRC = s11.PROJECT / "src"
AUTO = s11.WORK / "avtomatizaciya"
SEED = ["Не работает проектор", "Нет интернета", "Замятие бумаги в принтере", "Не включается компьютер", "Не работает мышь"]


def api(method: str, path: str, token: str = "", body: dict | None = None) -> dict:
    req = urllib.request.Request(f"{PB}{path}", method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json", "Authorization": token})
    raw = urllib.request.urlopen(req).read()
    return json.loads(raw) if raw else {}


def reset_db() -> None:
    """Пять заявок конца главы 2.2, все «Новая»."""
    token = api("POST", "/api/collections/_superusers/auth-with-password", body={"identity": EMAIL, "password": PASSWORD})["token"]
    for item in api("GET", "/api/collections/requests/records?perPage=200", token)["items"]:
        if item["title"] not in SEED:
            api("DELETE", f"/api/collections/requests/records/{item['id']}", token)
        elif item["status"] != "Новая":
            api("PATCH", f"/api/collections/requests/records/{item['id']}", token, {"status": "Новая"})


def reset() -> None:
    reset21()
    shutil.copy(Path(__file__).parent / "code21/App.tsx", SRC / "App.tsx")
    (SRC / "api.ts").unlink(missing_ok=True)


def put(name: str, dest: str) -> None:
    shutil.copy(CODE / name, SRC / dest)


def docker(*args: str) -> None:
    subprocess.run(["docker", "compose", *args], cwd=AUTO, capture_output=True)


async def wait_pb() -> None:
    for _ in range(60):
        try:
            if urllib.request.urlopen(f"{PB}/api/health").status == 200:
                return
        except Exception:
            pass
        await asyncio.sleep(1)
    raise SystemExit("PocketBase не запустился")


async def network_tab(br: s15.Browser) -> None:
    # Панели Network нужна высота: строки запросов идут под полосой времени.
    await br.dt.set_viewport_size({"width": 1100, "height": 400})
    await br.dt.get_by_role("tab", name="Network").click()
    await br.dt.wait_for_timeout(800)
    try:
        await br.dt.get_by_text("Fetch/XHR", exact=True).first.click(timeout=3000)
    except Exception:
        print("  ! фильтр Fetch/XHR не найден")
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

        # §2. Модуль api.ts с первой функцией.
        put("api-load.ts", "api.ts")
        await s14.reveal(ed, "zayavki/src/api.ts")
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await go_line(ed, 1)
        await ed.shot(str(IMG / "01-api-ts.png"))

        # §3. requests.ts без initialRequests, storage.ts удалён, App с загрузкой.
        put("requests.ts", "requests.ts")
        put("index.css", "index.css")
        (SRC / "storage.ts").unlink()
        put("App-load.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/requests.ts")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "02-requests-ts.png"))
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 22)
        await ed.shot(str(IMG / "03-app-load.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.full(IMG / "04-doska-server.png")

        # Медленная сеть: надпись «Загрузка заявок…» и два запроса в Network.
        await br.devtools()
        await network_tab(br)
        # Медленный ответ сервера: запрос к API задерживается на 4 секунды.
        async def slow(route):
            await asyncio.sleep(4)
            await route.continue_()
        await br.page.route("**/api/collections/**", slow)
        await br.page.goto(s14.URL, wait_until="commit")
        await br.page.wait_for_selector("text=Загрузка заявок", timeout=30000)
        await br.page.wait_for_timeout(600)
        await br.shot(IMG / "05-zagruzka.png", console=True)
        await br.page.wait_for_timeout(4000)
        await br.page.unroute("**/api/collections/**")
        await br.dt.locator('[aria-label="Clear network log"]').first.click()
        await br.load()
        await br.page.wait_for_timeout(1500)
        await br.shot(IMG / "06-network-dva.png", console=True)

        # Добавленная заявка пропадает после F5.
        await br.dt.close()
        br.dt = None
        await br.load()
        await s16.fill(br, "Не печатает принтер", "112", "Принтер", "")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.page.wait_for_timeout(1200)
        await br.full(IMG / "07-dobavlena-lokalno.png")
        await br.load()
        await br.full(IMG / "08-posle-f5.png")

        # §4. Сервер остановлен: вечная загрузка и ошибка в консоли.
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd avtomatizaciya", 1)
        await s11.terminal(ed, "docker compose stop pocketbase", 8)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "09-stop.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
        await ed.palette("View: Close Panel", 1)
        await br.devtools()
        await br.load()
        await br.page.wait_for_timeout(2000)
        await br.shot(IMG / "10-vechnaya-zagruzka.png", console=True)

        put("App-error.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 35)
        await ed.shot(str(IMG / "11-app-error.png"))
        await asyncio.sleep(1.5)
        await br.dt.close()
        br.dt = None
        await br.load()
        await br.page.wait_for_timeout(1500)
        await br.full(IMG / "12-oshibka.png")

        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd avtomatizaciya", 1)
        await s11.terminal(ed, "docker compose start pocketbase", 6)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "13-start.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
        await ed.palette("View: Close Panel", 1)
        await wait_pb()
        await br.page.get_by_role("button", name="Повторить").click()
        await br.page.wait_for_timeout(1500)
        await br.full(IMG / "14-povtorit.png")

        # §5. Изменения уходят на сервер.
        put("api.ts", "api.ts")
        put("App.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/api.ts")
        await go_line(ed, 30)
        await ed.shot(str(IMG / "15-api-full.png"))
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 92)
        await ed.shot(str(IMG / "16-app-final.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await s16.fill(br, "Не печатает принтер", "112", "Принтер", "")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.page.wait_for_timeout(1500)
        await br.click("Взять в работу", 0)
        await br.page.wait_for_timeout(800)
        await br.full(IMG / "17-dobavlena-server.png")
        await br.load()
        await br.full(IMG / "18-server-posle-f5.png")

        # Панель PocketBase: шесть записей.
        pb = await br.ctx.new_page()
        await pb.set_viewport_size({"width": 1280, "height": 800})
        await pb.goto(f"{PB}/_/")
        await pb.wait_for_timeout(2500)
        await pb.locator("input[type=email]").fill(EMAIL)
        await pb.locator("input[type=password]").fill(PASSWORD)
        await pb.keyboard.press("Enter")
        await pb.wait_for_timeout(2500)
        await pb.goto(f"{PB}/_/#/collections?collection=requests")
        await pb.wait_for_timeout(2500)
        await pb.screenshot(path=str(IMG / "19-panel.png"))
        print(f"  ✓ {IMG / '19-panel.png'}")
        await pb.close()

        # Ошибка действия: сервер остановлен, кнопка «Взять в работу».
        docker("stop", "pocketbase")
        await br.click("Взять в работу", 0)
        await br.page.wait_for_timeout(1500)
        await br.shot(IMG / "20-oshibka-deystviya.png")
        docker("start", "pocketbase")
        await wait_pb()

        await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: all")
