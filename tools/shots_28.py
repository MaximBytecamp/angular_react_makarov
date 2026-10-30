"""Кадры страницы «Автоматизация модуля 2: ИИ-диспетчер и кнопка «Взять»».

Продолжает папку студента react-kurs/avtomatizaciya после главы 2.5: n8n с процессом модуля 1 и
учётными данными бота, PocketBase с коллекцией requests. Модель qwen2.5:3b уже есть в томе Ollama.
Токен бота на кадр не попадает: в .env на время кадра записан образец, номер чата размывается.
Снимки Telegram — от автора (tools/n8n2/tg-*.png), имя на последнем размыто.

    N8N_TG_CHAT_FILE=… python3 tools/shots_28.py all
"""
import asyncio
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from urllib.parse import quote
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_14 as s14  # noqa: E402
import shots_15 as s15  # noqa: E402
import shots_16 as s16  # noqa: E402
import shots_23 as s23  # noqa: E402
from shots_13 import go_line  # noqa: E402
from shots_22 import EMAIL, PASSWORD  # noqa: E402
from shots_n8n import blur, wait_n8n  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/28-ii-dispetcher/img/raw"
TOOLS = Path(__file__).parent
AUTO = s11.WORK / "avtomatizaciya"
N8N = "http://localhost:5678"
PB = "http://localhost:8090/api/collections/requests/records"
DISPATCHER = (TOOLS / "n8n2/ii-dispetcher.json").read_text()
BUTTON = (TOOLS / "n8n2/knopka-vzyat.json").read_text()
TITLE = "Не показывает экран на стене"
ENV_SAMPLE = "TELEGRAM_TOKEN=1234567890:ваш-токен-от-BotFather\n"


def chat_id() -> str:
    return Path(os.environ["N8N_TG_CHAT_FILE"]).read_text().strip()


def superuser() -> str:
    return s23.api("POST", "/api/collections/_superusers/auth-with-password",
                   body={"identity": EMAIL, "password": PASSWORD})["token"]


def drop_test_records() -> None:
    token = superuser()
    path = "/api/collections/requests/records"
    for item in s23.api("GET", f"{path}?perPage=200", token)["items"]:
        if item["title"] == TITLE:
            s23.api("DELETE", f"{path}/{item['id']}", token)


async def login(pg) -> None:
    await pg.goto(f"{N8N}/signin")
    await pg.wait_for_timeout(2500)
    await pg.locator("input").first.fill("student@example.com")
    await pg.fill("input[type=password]", "Zayavki2026")
    await pg.keyboard.press("Enter")
    await pg.wait_for_timeout(3000)


async def rest(pg, method: str, path: str) -> dict:
    """Запрос к внутреннему API n8n из вошедшей вкладки: нужен заголовок browser-id."""
    return await pg.evaluate("""([m, p]) => fetch(p, {method: m, headers: {'browser-id': localStorage.getItem('n8n-browserId')}})
        .then(r => r.text()).then(t => t ? JSON.parse(t) : {})""", [method, path])


async def paste_workflow(pg, template: str) -> None:
    await pg.goto(f"{N8N}/workflow/new")
    await pg.wait_for_timeout(3000)
    await pg.evaluate("t => navigator.clipboard.writeText(t)", template)
    await pg.mouse.click(700, 450)
    await pg.keyboard.press("ControlOrMeta+V")
    await pg.wait_for_timeout(1500)
    skip = pg.get_by_role("button", name="Skip")
    if await skip.count():
        await skip.click()
        await pg.wait_for_timeout(1500)
    await pg.keyboard.press("ControlOrMeta+S")
    await pg.wait_for_timeout(2000)
    await pg.keyboard.press("Shift+1")  # уместить процесс в окно
    await pg.wait_for_timeout(800)


async def publish(pg) -> None:
    await pg.get_by_role("button", name="Publish").first.click()
    await pg.wait_for_timeout(1500)
    await pg.get_by_role("dialog").get_by_role("button", name="Publish").click()
    await pg.wait_for_timeout(2500)


async def all_frames() -> None:
    drop_test_records()
    shutil.copy(TOOLS / "code28/compose.yaml", AUTO / "compose.yaml")
    real_env = (AUTO / ".env").read_text()

    # VS Code: compose.yaml, .env с образцом токена, запуск и проверка модели.
    cdp.launch(str(s11.WORK))
    await asyncio.sleep(4)
    try:
        (AUTO / ".env").write_text(ENV_SAMPLE)
        async with cdp.Editor() as ed:
            await ed.size(1240, 780)
            await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
            await ed.palette("View: Close All Editors", 1.0)
            await ed.palette("View: Collapse Folders in Explorer", 1.0)
            await ed.palette("View: Show Explorer", 1.2)
            await s14.reveal(ed, "avtomatizaciya/compose.yaml")
            await ed.palette("File: Reveal Active File in Explorer View", 1.0)
            await go_line(ed, 14)
            await ed.shot(str(IMG / "b01-compose.png"))
            await s14.reveal(ed, "avtomatizaciya/.env")
            await go_line(ed, 1)
            await ed.shot(str(IMG / "b02-env.png"))
            await ed.palette("View: Close All Editors", 1.0)
            await s11.open_terminal(ed)
            await s11.terminal(ed, "cd zayavki && npm run dev", 6)
            await s11.open_terminal(ed)
            await s11.terminal(ed, "cd avtomatizaciya", 1)
            # На кадре образец токена: n8n перезапускается с ним только на время кадра.
            await s11.terminal(ed, "docker compose up -d", 10)
            await s11.terminal(ed, "docker compose ps", 3)
            await ed.palette("View: Toggle Maximized Panel", 1.5)
            await ed.shot(str(IMG / "b03-compose-up.png"))
            await s11.terminal(ed, "clear", 0.6)
            await s11.terminal(ed, "docker compose exec ollama ollama list", 3)
            await ed.shot(str(IMG / "b04-ollama-list.png"))
            await s11.terminal(ed, "clear", 0.6)
            await s11.terminal(ed, 'docker compose exec ollama ollama run qwen2.5:3b "Одним словом: к какой категории относится заявка «не включается проектор» — Компьютер, Проектор, Принтер или Интернет?"', 25)
            await ed.shot(str(IMG / "b05-ollama-run.png"))
            await ed.palette("View: Toggle Maximized Panel", 1.0)
            await ed.palette("View: Close Panel", 1)
    finally:
        (AUTO / ".env").write_text(real_env)
    subprocess.run(["docker", "compose", "up", "-d"], cwd=AUTO, capture_output=True)
    await wait_n8n()
    await asyncio.sleep(5)

    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2,
                                  permissions=["clipboard-read", "clipboard-write"])
        pg = await ctx.new_page()

        async def shot(name: str) -> Path:
            await pg.wait_for_timeout(700)
            path = IMG / name
            await pg.screenshot(path=str(path))
            print(f"  ✓ {path}")
            return path

        await login(pg)
        # Процессы, импортированные при проверке, удаляются: студент вставляет шаблоны сам.
        for w in (await rest(pg, "GET", "/rest/workflows"))["data"]:
            if w["name"] in ("ИИ-диспетчер", "Кнопка «Взять»"):
                await rest(pg, "POST", f"/rest/workflows/{w['id']}/deactivate")
                await rest(pg, "POST", f"/rest/workflows/{w['id']}/archive")
                await rest(pg, "DELETE", f"/rest/workflows/{w['id']}")
        a1 = next(w["id"] for w in (await rest(pg, "GET", "/rest/workflows"))["data"] if w["name"] == "Заявка → Telegram")

        # Процесс модуля 1 снимается с публикации: тот же адрес вебхука.
        await pg.goto(f"{N8N}/workflow/{a1}")
        await pg.wait_for_timeout(3500)
        await pg.locator('[data-test-id="version-menu-button"]').click()
        await pg.wait_for_timeout(800)
        await shot("b06-unpublish.png")
        await pg.get_by_text("Unpublish", exact=True).click()
        await pg.wait_for_timeout(1500)
        confirm = pg.get_by_role("dialog").get_by_role("button", name="Unpublish")
        if await confirm.count():
            await confirm.click()
            await pg.wait_for_timeout(1500)

        # Процесс «ИИ-диспетчер».
        await paste_workflow(pg, DISPATCHER)
        await shot("b07-canvas-dispetcher.png")
        await pg.locator('[data-test-id="canvas-node"]', has_text="Модель").dblclick()
        await pg.wait_for_timeout(1500)
        await shot("b08-model.png")
        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(800)
        await pg.locator('[data-test-id="canvas-node"]', has_text="Telegram").dblclick()
        await pg.wait_for_timeout(1500)
        chat = pg.locator('[data-test-id="parameter-input-chatId"] input').first
        await chat.click()
        await pg.keyboard.type(chat_id())
        await pg.get_by_text("Parameters").first.click()
        await pg.wait_for_timeout(600)
        box = await chat.bounding_box()
        path = await shot("b09-telegram.png")
        blur(path, [(box["x"] + 8, box["y"] + 4, 160, box["height"] - 8)])
        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(800)
        await pg.keyboard.press("ControlOrMeta+S")
        await pg.wait_for_timeout(1500)
        await publish(pg)
        await shot("b10-published-dispetcher.png")
        dispatcher_url = pg.url.split("?")[0]

        await part2(pg, ctx, dispatcher_url)
        await b.close()


async def part2(pg, ctx, dispatcher_url: str) -> None:
    """Второй процесс, проверка с доски и запуск в n8n."""
    async def shot(name: str) -> Path:
        await pg.wait_for_timeout(700)
        path = IMG / name
        await pg.screenshot(path=str(path))
        print(f"  ✓ {path}")
        return path

    # Процесс «Кнопка «Взять»».
    await paste_workflow(pg, BUTTON)
    await shot("b11-canvas-knopka.png")
    await pg.locator('[data-test-id="canvas-node"]').filter(has=pg.get_by_text("Нажатия", exact=True)).dblclick()
    await pg.wait_for_timeout(1500)
    await shot("b12-getupdates.png")
    await pg.keyboard.press("Escape")
    await pg.wait_for_timeout(800)
    await publish(pg)
    await shot("b13-published-knopka.png")

    # Заявка с доски: сразу после отправки и после ответа модели.
    br = s15.Browser()
    await br.start()
    await br.load()
    await s16.fill(br, TITLE, "214", "Компьютер", "Через 10 минут экзамен, изображения на стене нет.")
    await br.page.get_by_role("button", name="Отправить заявку").click()
    await br.page.wait_for_timeout(1500)
    await br.shot(IMG / "b14-doska-otpravleno.png")

    await pg.goto(f"{dispatcher_url}/executions")
    await pg.wait_for_timeout(20000)
    await pg.reload()
    await pg.wait_for_timeout(4000)
    close = pg.locator('[data-test-id="production-checklist"] button').first
    if await close.count():
        await close.click()
    await shot("b15-execution.png")
    await pg.locator('[data-test-id="canvas-node"]', has_text="Ответ модели").dblclick()
    await pg.wait_for_timeout(1500)
    await shot("b16-otvet-modeli.png")

    # Нажатие «Взять» делает человек в Telegram; на доске — его результат: статус «В работе».
    token = superuser()
    rec = s23.api("GET", "/api/collections/requests/records?filter=" + quote(f"title='{TITLE}'"), token)["items"][0]
    await br.page.wait_for_timeout(500)
    s23.api("PATCH", f"/api/collections/requests/records/{rec['id']}", token, {"status": "В работе"})
    await br.page.wait_for_timeout(1500)
    await br.shot(IMG / "b17-doska-v-rabote.png")
    await br.close()



async def only_part2() -> None:
    """Повтор со второго процесса: первый уже опубликован."""
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2,
                                  permissions=["clipboard-read", "clipboard-write"])
        pg = await ctx.new_page()
        await login(pg)
        dispatcher = None
        for w in (await rest(pg, "GET", "/rest/workflows"))["data"]:
            if w["name"] == "Кнопка «Взять»":
                await rest(pg, "POST", f"/rest/workflows/{w['id']}/archive")
                await rest(pg, "DELETE", f"/rest/workflows/{w['id']}")
            if w["name"] == "ИИ-диспетчер":
                dispatcher = w["id"]
        await part2(pg, ctx, f"{N8N}/workflow/{dispatcher}")
        await b.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    elif sys.argv[1:] == ["part2"]:
        asyncio.run(only_part2())
    else:
        raise SystemExit("стадии: all")
