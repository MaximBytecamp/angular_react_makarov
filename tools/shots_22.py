"""Кадры главы 2.2: PocketBase — коллекции и правила доступа.

PocketBase запускается в папке студента react-kurs/avtomatizaciya (tools/code22/compose.yaml,
tools/code22/pocketbase/Dockerfile) рядом с n8n из модуля 1. Перед съёмкой том PocketBase
удаляется: кадры снимаются с пустой базы. Панель администратора и ответы API снимаются
в headless Chromium, терминал — в VS Code (tools/cdp.py).

    python3 tools/shots_22.py all
"""
import asyncio
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
from shots_13 import go_line  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/22-pocketbase/img/raw"
CODE = Path(__file__).parent / "code22"
AUTO = s11.WORK / "avtomatizaciya"
PB = "http://localhost:8090"
EMAIL, PASSWORD = "admin@example.com", "Zayavki2026pb"

FIELDS = [
    ("Plain text", "title", True, []),
    ("Plain text", "room", True, []),
    ("Select", "category", True, ["Компьютер", "Проектор", "Принтер", "Интернет"]),
    ("Plain text", "details", False, []),
    ("Select", "status", True, ["Новая", "В работе", "Готово"]),
]
RULES = {
    "listRule": "",
    "viewRule": "",
    "createRule": '@request.body.status = "Новая"',
    "updateRule": "@request.body.title:isset = false && @request.body.room:isset = false"
                   " && @request.body.details:isset = false",
    "deleteRule": 'status = "Готово"',
}

TEST_GOTOVO = """await fetch('/api/collections/requests/records', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Проверка правил', room: '101', category: 'Компьютер', status: 'Готово' }),
}).then((r) => r.json())"""
TEST_TITLE = """const list = await fetch('/api/collections/requests/records').then((r) => r.json())
await fetch('/api/collections/requests/records/' + list.items[0].id, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Чужое название' }),
}).then((r) => r.json())"""


def sh(*args: str) -> str:
    run = subprocess.run(list(args), cwd=AUTO, capture_output=True, text=True)
    return run.stdout + run.stderr


async def wait_pb() -> None:
    for _ in range(60):
        try:
            if urllib.request.urlopen(f"{PB}/api/health").status == 200:
                return
        except Exception:
            pass
        await asyncio.sleep(1)
    raise SystemExit("PocketBase не запустился")


async def all_frames() -> None:
    (AUTO / "pocketbase").mkdir(parents=True, exist_ok=True)
    shutil.copy(CODE / "compose.yaml", AUTO / "compose.yaml")
    shutil.copy(CODE / "pocketbase/Dockerfile", AUTO / "pocketbase/Dockerfile")
    print(sh("docker", "compose", "rm", "-sf", "pocketbase"))
    print(sh("docker", "volume", "rm", "avtomatizaciya_pb_data"))

    cdp.launch(str(s11.WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1240, 780)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await ed.palette("View: Show Explorer", 1.2)
        # Открытие App.tsx обновляет проверку типов: иначе VS Code показывает ошибки прошлого сеанса.
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await asyncio.sleep(4)
        await ed.palette("View: Close All Editors", 1.0)
        await ed.palette("View: Collapse Folders in Explorer", 1.0)
        await ed.palette("View: Close Panel", 1.0)
        await s14.reveal(ed, "avtomatizaciya/pocketbase/Dockerfile")
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await go_line(ed, 1)
        await ed.shot(str(IMG / "01-dockerfile.png"))
        await s14.reveal(ed, "avtomatizaciya/compose.yaml")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "02-compose.png"))
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd avtomatizaciya", 1)
        await s11.terminal(ed, "docker compose up -d --build", 25)
        await s11.terminal(ed, "clear", 0.6)
        await s11.terminal(ed, "docker compose ps", 3)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "03-compose-ps.png"))
        await wait_pb()
        await s11.terminal(ed, "clear", 0.6)
        await s11.terminal(ed, f"docker compose exec pocketbase /pb/pocketbase superuser upsert {EMAIL} {PASSWORD} --dir=/pb/pb_data", 6)
        await ed.shot(str(IMG / "04-superuser.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)

    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2)
        pg = await ctx.new_page()

        async def shot(name: str) -> None:
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(IMG / name))
            print(f"  ✓ {IMG / name}")

        # Вход в панель.
        await pg.goto(f"{PB}/_/")
        await pg.wait_for_timeout(2500)
        await pg.locator("input[type=email]").fill(EMAIL)
        await pg.locator("input[type=password]").fill(PASSWORD)
        await shot("05-login.png")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(2500)
        await shot("06-dashboard.png")

        # Коллекция requests.
        await pg.get_by_role("button", name="New collection").click()
        await pg.wait_for_timeout(1200)
        await pg.get_by_placeholder("e.g. posts").fill("requests")
        await pg.get_by_text("New field").click()
        await pg.wait_for_timeout(500)
        await shot("07-new-field.png")
        await pg.keyboard.press("Escape")
        for i, (kind, name, required, choices) in enumerate(FIELDS, start=1):
            await pg.get_by_text("New field").click()
            await pg.wait_for_timeout(400)
            await pg.get_by_text(kind, exact=True).first.click()
            await pg.wait_for_timeout(400)
            await pg.keyboard.type(name)
            if choices:
                await pg.get_by_placeholder("Add choices*").last.click()
                for c in choices:
                    await pg.keyboard.type(c)
                    await pg.keyboard.press("Enter")
                await pg.wait_for_timeout(300)
                await pg.mouse.click(900, 40)
            if required:
                row = pg.locator("details.record-field-settings").nth(i)
                await row.locator("summary button[title=\"Field options\"]").click()
                await pg.wait_for_timeout(400)
                if name == "title":
                    await shot("08-field-options.png")
                await row.get_by_text("Required", exact=False).first.click()
                await row.locator("summary button[title=\"Field options\"]").click()
                await pg.wait_for_timeout(300)
        await shot("09-fields.png")
        await pg.get_by_role("button", name="Create", exact=True).click()
        await pg.wait_for_timeout(2000)
        await shot("10-collection.png")

        # Первая запись через панель.
        await pg.get_by_role("button", name="New record").first.click()
        await pg.wait_for_timeout(1200)
        await pg.locator("textarea").and_(pg.get_by_label("title", exact=True)).fill("Не работает проектор")
        await pg.locator("textarea").and_(pg.get_by_label("room", exact=True)).fill("214")
        selects = pg.locator(".record-field-input.field-type-select")
        for i, value in enumerate(("Проектор", "Новая")):
            await selects.nth(i).locator("button.selected-container").click()
            await pg.wait_for_timeout(300)
            await pg.locator(".dropdown-item.select-option", has_text=value).first.click()
            await pg.wait_for_timeout(300)
        await pg.locator("textarea").and_(pg.get_by_label("details", exact=True)).fill("Проектор включается, но изображения на экране нет.")
        await shot("11-record-form.png")
        await pg.get_by_role("button", name="Create", exact=True).click()
        await pg.wait_for_timeout(1500)
        await shot("12-records.png")

        # Ответ API при закрытых правилах.
        api = await ctx.new_page()
        await api.set_viewport_size({"width": 1100, "height": 300})
        await api.goto(f"{PB}/api/collections/requests/records")
        await api.wait_for_timeout(800)
        await api.screenshot(path=str(IMG / "13-api-403.png"))
        print("  ✓ 13-api-403")

        # Правила доступа.
        await pg.locator("button[title='Edit collection'], button[aria-label='Edit collection']").first.click() \
            if await pg.locator("button[title='Edit collection'], button[aria-label='Edit collection']").count() \
            else await pg.mouse.click(503, 81)
        await pg.wait_for_timeout(1200)
        await pg.get_by_text("API rules", exact=True).click()
        await pg.wait_for_timeout(1000)
        for name, rule in RULES.items():
            field = pg.locator(f'div.rule-field[name="{name}"]')
            await field.locator("button.unlock-overlay").click()
            await pg.wait_for_timeout(300)
            if rule:
                await field.locator(".code-editor-content").click()
                await pg.keyboard.insert_text(rule)
                await pg.wait_for_timeout(200)
        await pg.mouse.click(900, 250)
        await shot("14-rules.png")
        await pg.get_by_role("button", name="Save changes").click()
        await pg.wait_for_timeout(1500)
        confirm = pg.get_by_role("button", name="Confirm")
        if await confirm.count():
            await confirm.click()
            await pg.wait_for_timeout(1200)

        await api.goto(f"{PB}/api/collections/requests/records")
        await api.wait_for_timeout(800)
        await api.set_viewport_size({"width": 1100, "height": 360})
        await api.screenshot(path=str(IMG / "15-api-list.png"))
        print("  ✓ 15-api-list")
        await b.close()

    # Консоль браузера на странице API: проверка правил и остальные заявки.
    s14.URL = f"{PB}/api/collections/requests/records"
    br = s15.Browser()
    await br.start()
    await br.page.goto(s14.URL)
    await br.page.wait_for_timeout(800)
    await br.devtools()

    async def run(code: str) -> None:
        prompt = br.dt.locator(".console-prompt-editor-container").first
        await prompt.click()
        await br.dt.evaluate("t => navigator.clipboard && 0", code)
        await br.dt.keyboard.insert_text(code)
        await br.dt.keyboard.press("Enter")
        await br.dt.wait_for_timeout(2500)

    await br.dt.set_viewport_size({"width": 1100, "height": 420})
    await run(TEST_GOTOVO)
    await br.dt.screenshot(path=str(IMG / "16-console-gotovo.png"))
    print("  ✓ 16-console-gotovo")
    await br.dt.locator('[aria-label="Clear console"]').first.click()
    await run((CODE / "seed.js").read_text())
    await br.dt.screenshot(path=str(IMG / "17-console-seed.png"))
    print("  ✓ 17-console-seed")
    await br.dt.locator('[aria-label="Clear console"]').first.click()
    await run(TEST_TITLE)
    await br.dt.screenshot(path=str(IMG / "18-console-title.png"))
    print("  ✓ 18-console-title")
    await br.close()

    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2)
        pg = await ctx.new_page()
        await pg.goto(f"{PB}/_/")
        await pg.wait_for_timeout(2000)
        await pg.locator("input[type=email]").fill(EMAIL)
        await pg.locator("input[type=password]").fill(PASSWORD)
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(2000)
        await pg.goto(f"{PB}/_/#/collections?collection=requests")
        await pg.wait_for_timeout(2000)
        await pg.screenshot(path=str(IMG / "19-records-five.png"))
        print("  ✓ 19-records-five")
        await b.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: all")
