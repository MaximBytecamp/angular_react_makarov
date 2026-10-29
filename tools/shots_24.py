"""Кадры главы 2.4: собственный хук useRequests.

Продолжает проект zayavki после главы 2.3 (tools/code23) и PocketBase с шестью заявками
конца главы 2.3. Перед съёмкой база приводится к этим шести заявкам.

    python3 tools/shots_24.py all
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
import shots_23 as s23  # noqa: E402
from shots_13 import go_line  # noqa: E402
from shots_21 import reset as reset21  # noqa: E402
from shots_22 import EMAIL, PASSWORD  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/24-sobstvennyy-huk/img/raw"
C23 = Path(__file__).parent / "code23"
CODE = Path(__file__).parent / "code24"
SRC = s11.PROJECT / "src"
PRINTER = "Не печатает принтер"


def reset_db() -> None:
    """Шесть заявок конца главы 2.3: пять «Новая» и «Не печатает принтер» в работе."""
    token = s23.api("POST", "/api/collections/_superusers/auth-with-password",
                    body={"identity": EMAIL, "password": PASSWORD})["token"]
    path = "/api/collections/requests/records"
    items = s23.api("GET", f"{path}?perPage=200", token)["items"]
    for item in items:
        if item["title"] not in s23.SEED + [PRINTER]:
            s23.api("DELETE", f"{path}/{item['id']}", token)
        elif item["title"] in s23.SEED and item["status"] != "Новая":
            s23.api("PATCH", f"{path}/{item['id']}", token, {"status": "Новая"})
    if not any(i["title"] == PRINTER for i in items):
        rec = s23.api("POST", path, token, {"title": PRINTER, "room": "112", "category": "Принтер",
                                            "details": "", "status": "Новая"})
        s23.api("PATCH", f"{path}/{rec['id']}", token, {"status": "В работе"})


def reset() -> None:
    """Проект конца главы 2.3."""
    reset21()
    (SRC / "storage.ts").unlink(missing_ok=True)
    (SRC / "useRequests.ts").unlink(missing_ok=True)
    for name in ("App.tsx", "api.ts", "requests.ts", "index.css"):
        shutil.copy(C23 / name, SRC / name)


def put(name: str, dest: str) -> None:
    shutil.copy(CODE / name, SRC / dest)


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

        # §2. Хук с загрузкой.
        put("useRequests-load.ts", "useRequests.ts")
        put("App-load.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/useRequests.ts")
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await go_line(ed, 20)
        await ed.shot(str(IMG / "01-hook-load.png"))
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 18)
        await ed.shot(str(IMG / "02-app-load.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.full(IMG / "03-doska.png")

        # §3. Действия в хуке.
        put("useRequests.ts", "useRequests.ts")
        put("App.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/useRequests.ts")
        await go_line(ed, 42)
        await ed.shot(str(IMG / "04-hook-full.png"))
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 52)
        await ed.shot(str(IMG / "05-app-final.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await s16.fill(br, "Нет звука в колонках", "305", "Компьютер", "")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.page.wait_for_timeout(1500)
        await br.full(IMG / "06-dobavlena.png")

        # §4. Хук в двух компонентах: два запроса на каждый вызов и два разных списка.
        put("Header-hook.tsx", "components/Header.tsx")
        put("App-header-hook.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/components/Header.tsx")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "07-header-hook.png"))
        await asyncio.sleep(1.5)
        await br.devtools()
        await s23.network_tab(br)
        await br.load()
        await br.page.wait_for_timeout(1500)
        await br.shot(IMG / "08-network-chetyre.png", console=True)
        await br.dt.close()
        br.dt = None
        await br.load()
        await br.click("Взять в работу", 0)
        await br.page.wait_for_timeout(1200)
        await br.shot(IMG / "09-rassinhron.png")
        shutil.copy(Path(__file__).parent / "code14/Header.tsx", SRC / "components/Header.tsx")
        put("App.tsx", "App.tsx")

        # §5. Хук после раннего return: линтер и ошибка в браузере.
        put("App-ranniy-return.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 18)
        await ed.shot(str(IMG / "10-ranniy-return.png"))
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki && npm run lint", 5)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "11-lint-return.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
        await ed.palette("View: Close Panel", 1)
        await asyncio.sleep(1.0)
        await br.devtools()
        await br.load()
        await br.dt.locator('[aria-label="Clear console"]').first.click()
        await br.page.locator(".filters button", has_text="Готово").click()
        await br.page.wait_for_timeout(1500)
        await br.shot(IMG / "12-gotovo-oshibka.png", console=True)

        put("App.tsx", "App.tsx")
        await asyncio.sleep(1.0)
        await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: all")
