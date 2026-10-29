"""Кадры страницы «Автоматизация: заявка → n8n → Telegram».

n8n запускается из папки студента react-kurs/avtomatizaciya командой docker compose,
как в шагах страницы; перед съёмкой том с данными n8n удаляется, чтобы снять первый вход.
Токен бота читается из файла (путь в N8N_TG_TOKEN_FILE) и вводится в поле-пароль:
на кадрах видны только точки. Номер чата на кадрах размывается (blur).

    N8N_TG_TOKEN_FILE=… python3 tools/shots_n8n.py all
"""
import asyncio
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_14 as s14  # noqa: E402
import shots_15 as s15  # noqa: E402
from shots_13 import go_line  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/18-avtomatizaciya/img/raw"
AUTO = s11.WORK / "avtomatizaciya"
N8N = "http://localhost:5678"
TEMPLATE = (Path(__file__).parent / "n8n/zayavka-telegram.json").read_text()


def token() -> str:
    return Path(os.environ["N8N_TG_TOKEN_FILE"]).read_text().strip()


def chat_id() -> str:
    """Номер чата: из файла N8N_TG_CHAT_FILE, иначе из getUpdates."""
    saved = os.environ.get("N8N_TG_CHAT_FILE")
    if saved:
        return Path(saved).read_text().strip()
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token()}/getUpdates") as r:
        data = json.load(r)
    return str(data["result"][-1]["message"]["chat"]["id"])


def blur(path: Path, boxes: list[tuple[float, float, float, float]], scale: int = 2) -> None:
    """Размывает прямоугольники (в пикселях CSS) на снимке двойной плотности."""
    im = Image.open(path)
    for x, y, w, h in boxes:
        box = tuple(int(v * scale) for v in (x, y, x + w, y + h))
        im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
    im.save(path)


def compose(*args: str) -> str:
    run = subprocess.run(["docker", "compose", *args], cwd=AUTO, capture_output=True, text=True)
    return run.stdout + run.stderr


async def wait_n8n() -> None:
    for _ in range(90):
        try:
            if urllib.request.urlopen(f"{N8N}/healthz").status == 200:
                return
        except Exception:
            pass
        await asyncio.sleep(2)
    raise SystemExit("n8n не запустился")


async def all_frames() -> None:
    AUTO.mkdir(exist_ok=True)
    shutil.copy(Path(__file__).parent / "n8n/compose.yaml", AUTO / "compose.yaml")
    print(compose("down", "-v"))

    # VS Code: compose.yaml и запуск в терминале.
    cdp.launch(str(s11.WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1240, 780)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await ed.palette("View: Show Explorer", 1.2)
        await s14.reveal(ed, "avtomatizaciya/compose.yaml")
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await go_line(ed, 1)
        await ed.shot(str(IMG / "a01-compose.png"))
        # Первый терминал — сервер разработки доски, второй — для docker compose.
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki && npm run dev", 6)
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd avtomatizaciya", 1)
        await s11.terminal(ed, "docker compose up -d", 8)
        await s11.terminal(ed, "docker compose ps", 3)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "a02-compose-up.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
    await wait_n8n()

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

        # Первый вход: учётная запись владельца.
        await pg.goto(f"{N8N}/")
        await pg.wait_for_timeout(3000)
        await pg.fill("input[name=email]", "student@example.com")
        await pg.fill("input[name=firstName]", "Иван")
        await pg.fill("input[name=lastName]", "Петров")
        await pg.fill("input[name=password]", "Zayavki2026")
        await shot("a03-setup.png")
        await pg.get_by_role("button", name="Next").click()
        await pg.wait_for_timeout(3000)
        await shot("a04-survey.png")
        await pg.locator('[data-test-id="personalization-form"]').get_by_role("button", name="Get started").click()
        await pg.wait_for_timeout(2000)
        await pg.goto(f"{N8N}/home/workflows")
        await pg.wait_for_timeout(2500)
        await shot("a05-home.png")

        # Шаблон процесса: вставка на пустой холст.
        await pg.get_by_text("Build a workflow").click()
        await pg.wait_for_timeout(3000)
        await pg.evaluate("t => navigator.clipboard.writeText(t)", TEMPLATE)
        await pg.mouse.click(700, 450)
        await pg.keyboard.press("ControlOrMeta+V")
        await pg.wait_for_timeout(1500)
        # Окно «Pasting this from an AI tool?» n8n показывает не при каждой вставке.
        skip = pg.get_by_role("button", name="Skip")
        if await skip.count():
            await shot("a06-paste-ai.png")
            await skip.click()
            await pg.wait_for_timeout(1500)
        await pg.keyboard.press("ControlOrMeta+S")
        await pg.wait_for_timeout(1500)
        await shot("a07-canvas.png")

        # Узел Webhook.
        await pg.locator('[data-test-id="canvas-node"]', has_text="Webhook").dblclick()
        await pg.wait_for_timeout(1500)
        await shot("a08-webhook.png")
        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(800)

        # Узел Telegram: токен и номер чата.
        await pg.locator('[data-test-id="canvas-node"]', has_text="Telegram").dblclick()
        await pg.wait_for_timeout(1500)
        await shot("a09-telegram.png")
        await pg.get_by_text("Connect to Telegram").click()
        await pg.wait_for_timeout(1500)
        await pg.locator("input[type=password]").fill(token())
        await pg.get_by_role("button", name="Save").first.click()
        await pg.wait_for_timeout(2500)
        await shot("a10-credential.png")
        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(1000)

        # Номер чата — из ответа getUpdates; адрес с токеном в кадр не попадает.
        api = await ctx.new_page()
        await api.set_viewport_size({"width": 1100, "height": 520})
        for attempt in range(5):
            try:
                await api.goto(f"https://api.telegram.org/bot{token()}/getUpdates")
                break
            except Exception:
                print("  getUpdates: повтор", attempt + 1)
                await api.wait_for_timeout(3000)
        await api.wait_for_timeout(1500)
        cid = chat_id()
        # Красивый вид JSON у Chrome — флажок Pretty-print; иначе одна строка.
        pretty = api.get_by_text("Pretty-print")
        if await pretty.count():
            await pretty.click()
            await api.wait_for_timeout(500)
        boxes = await api.evaluate("""id => {
            const out = [];
            const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            while (walk.nextNode()) {
                const n = walk.currentNode; let i = n.data.indexOf(id);
                while (i >= 0) {
                    const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + id.length);
                    for (const b of r.getClientRects()) out.push([b.x - 2, b.y - 2, b.width + 4, b.height + 4]);
                    i = n.data.indexOf(id, i + 1);
                }
            }
            return out;
        }""", cid)
        path = IMG / "a11-getupdates.png"
        await api.screenshot(path=str(path))
        blur(path, boxes)
        print(f"  ✓ {path} (размыто мест: {len(boxes)})")
        await api.close()

        chat = pg.locator('[data-test-id="parameter-input-chatId"] input').first
        if not await chat.is_visible():
            await pg.locator('[data-test-id="canvas-node"]', has_text="Telegram").dblclick()
            await pg.wait_for_timeout(1500)
        await chat.click()
        await pg.keyboard.type(cid)
        await pg.get_by_text("Parameters").first.click()
        await pg.wait_for_timeout(600)
        box = await chat.bounding_box()
        path = await shot("a12-chat-id.png")
        blur(path, [(box["x"] + 8, box["y"] + 4, 160, box["height"] - 8)])
        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(800)
        await pg.keyboard.press("ControlOrMeta+S")
        await pg.wait_for_timeout(1500)

        # Публикация.
        await pg.get_by_role("button", name="Publish").first.click()
        await pg.wait_for_timeout(1500)
        await shot("a13-publish.png")
        await pg.get_by_role("dialog").get_by_role("button", name="Publish").click()
        await pg.wait_for_timeout(2500)
        await shot("a14-published.png")
        workflow_url = pg.url.split("?")[0]

        # Заявка с доски.
        br = s15.Browser()
        await br.start()
        await br.load()
        await br.page.evaluate("localStorage.clear()")
        await br.load()
        await s16_fill(br)
        await br.page.wait_for_timeout(2500)
        await br.full(IMG / "a15-otpravleno.png")
        await br.close()

        # Список запусков.
        await pg.goto(f"{workflow_url}/executions")
        await pg.wait_for_timeout(25000)
        await pg.reload()
        await pg.wait_for_timeout(4000)
        close = pg.locator('[data-test-id="production-checklist"] button').first
        if await close.count():
            await close.click()
        await shot("a16-executions.png")
        await b.close()


async def s16_fill(br: s15.Browser) -> None:
    p = br.page
    await p.locator("#title").press_sequentially("Не работает проектор в актовом зале", delay=10)
    await p.locator("#room").press_sequentially("Актовый зал", delay=10)
    await p.locator("#category").select_option("Проектор")
    await p.locator("#details").press_sequentially("Проектор не видит ноутбук, кабель HDMI подключён.", delay=5)
    await p.get_by_role("button", name="Отправить заявку").click()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: all")
