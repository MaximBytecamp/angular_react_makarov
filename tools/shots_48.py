"""Кадры автоматизации модуля 4: Google Таблица и Apps Script, процессы n8n дайджеста.

Страницы Google снимаются в Chrome автора с входом в аккаунт (профиль ~/firebase-shots-chrome, порт отладки 9391):
таблица «Дайджест новостей» и проект Apps Script «Дайджест». Значение ключа на кадре свойств замазывается.
n8n — стенд tools/code45/stand (localhost:5678, владелец student@example.org, пароль в ~/digest-n8n-pass.txt).
Терминал — VS Code из shots_33 (профиль vsc-react).

    python3 tools/shots_48.py google | n8n | terminal
"""
import asyncio
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_33 as s33  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/48-avtomatizaciya/img/raw"
s33.IMG = IMG
cdp.PORT = 9362
SHEET = "1Q7robqIYt_J7xxjf7Xt1cNiG1GzcJFq3uC_THjlyKcs"
SCRIPT = "1bEw-7LV5kdl8CKUE9kSknx6WM0oHlt5IHM68HVz_ID3W_KUTWhQcPMAJ"
N8N = "http://localhost:5678"


def blur(path: Path, box: tuple) -> None:
    """Скрывает фрагмент кадра: сильное размытие, затем полупрозрачная заливка — символы не читаются."""
    im = Image.open(path).convert("RGB")
    part = im.crop(box).filter(ImageFilter.GaussianBlur(30))
    part = Image.blend(part, Image.new("RGB", part.size, "#e8eaed"), 0.6)
    im.paste(part, box[:2])
    im.save(path)


async def hide(page, path: Path, locator, pad: int = 2) -> None:
    bb = await locator.bounding_box()
    k = Image.open(path).width / page.viewport_size["width"]
    blur(path, tuple(int(v * k) for v in (bb["x"] - pad, bb["y"] - pad, bb["x"] + bb["width"] + pad, bb["y"] + bb["height"] + pad)))


async def shot(page, name: str) -> Path:
    path = IMG / name
    await page.wait_for_timeout(800)
    await page.screenshot(path=str(path))
    print(f"  ✓ {path}")
    return path


async def stage_google() -> None:
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp("http://localhost:9391")
        ctx = b.contexts[0]
        page = await ctx.new_page()
        await page.set_viewport_size({"width": 1240, "height": 760})

        await page.goto(f"https://script.google.com/home/projects/{SCRIPT}/edit", wait_until="domcontentloaded")
        await page.wait_for_timeout(7000)
        await shot(page, "02-apps-script.png")

        await page.goto(f"https://script.google.com/home/projects/{SCRIPT}/settings", wait_until="domcontentloaded")
        await page.wait_for_timeout(6000)
        await page.get_by_text("Свойства скрипта", exact=True).scroll_into_view_if_needed()
        await page.wait_for_timeout(800)
        path = await shot(page, "03-klyuch.png")
        await hide(page, path, page.locator("input:visible").last)

        await page.goto(f"https://script.google.com/home/projects/{SCRIPT}/edit", wait_until="domcontentloaded")
        await page.wait_for_timeout(7000)
        await page.locator("[role=button]:visible", has_text="Начать развертывание").click()
        await page.wait_for_timeout(1200)
        item = page.locator("[role=menuitem]:visible", has_text="Новое развертывание")
        bb = await item.bounding_box()
        await page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
        await page.wait_for_timeout(4000)
        dialog = page.locator("[role=dialog]:visible").first
        if "Запуск от имени" not in await dialog.inner_text():
            gear = dialog.locator('[aria-label="Включить типы развертывания"]')
            bb = await gear.bounding_box()
            await page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
            await page.wait_for_timeout(1200)
            await page.locator("[role=dialog]:visible").get_by_text("Веб-приложение", exact=True).first.click()
            await page.wait_for_timeout(2000)
        await page.locator("[role=dialog]:visible input:visible").first.fill("Первая версия")
        access = page.locator("[role=dialog]:visible [role=listbox]:visible, [role=dialog]:visible [aria-haspopup=listbox]:visible").last
        await access.click()
        await page.wait_for_timeout(1000)
        await page.locator("[role=option]:visible").filter(has_text="Все").first.click()
        await page.wait_for_timeout(1000)
        path = await shot(page, "04-razvertyvanie.png")
        await hide(page, path, page.locator("[role=dialog]:visible").get_by_text("@gmail.com").first)
        await page.locator("[role=dialog]:visible").get_by_role("button", name="Отмена").click()
        await page.wait_for_timeout(1500)

        await page.locator("[role=button]:visible", has_text="Начать развертывание").click()
        await page.wait_for_timeout(1200)
        item = page.locator("[role=menuitem]:visible", has_text="Управление развертываниями")
        bb = await item.bounding_box()
        await page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
        await page.locator("[role=dialog]:visible").get_by_text("/exec").first.wait_for(timeout=60000)
        await page.wait_for_timeout(1500)
        path = await shot(page, "06-url.png")
        mail = page.locator("[role=dialog]:visible").get_by_text("@gmail.com")
        if await mail.count():
            await hide(page, path, mail.first)
        await page.keyboard.press("Escape")

        await page.goto(f"https://docs.google.com/spreadsheets/d/{SHEET}/edit", wait_until="domcontentloaded")
        await page.wait_for_timeout(7000)
        await shot(page, "10-tablica-novosti.png")
        await page.close()


async def n8n_page(p):
    browser = await p.chromium.launch()
    page = await browser.new_page(viewport={"width": 1240, "height": 760}, device_scale_factor=2)
    await page.goto(f"{N8N}/signin")
    await page.wait_for_timeout(2000)
    await page.locator("input[type=email], input[name=emailOrLdapLoginId]").first.fill("student@example.org")
    await page.locator("input[type=password]").fill((Path.home() / "digest-n8n-pass.txt").read_text().strip())
    await page.keyboard.press("Enter")
    await page.wait_for_timeout(3000)
    return browser, page


async def stage_n8n() -> None:
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser, page = await n8n_page(p)
        await page.goto(f"{N8N}/workflow/aURQ89UefNu4wepF")
        await page.wait_for_timeout(4000)
        start = page.get_by_role("button", name="Get started")
        if await start.count():
            await start.click()
            await page.wait_for_timeout(1500)
        skip = page.get_by_role("button", name="Skip")
        if await skip.count():
            await skip.click()
            await page.wait_for_timeout(1500)
        banner = page.get_by_text("Get ready for n8n 3.0")
        if await banner.count():
            box = await banner.first.bounding_box()
            await page.mouse.click(1214, box["y"] + box["height"] / 2)
            await page.wait_for_timeout(800)
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(800)
        await page.keyboard.press("Shift+1")
        await page.wait_for_timeout(1000)
        await shot(page, "08-n8n-sbor.png")
        await page.get_by_text("Execute", exact=True).first.click()
        await page.wait_for_timeout(1500)
        manual = page.get_by_text("Запустить вручную", exact=True)
        if await page.locator(".el-dropdown-menu:visible, [role=menu]:visible").count():
            await page.locator(".el-dropdown-menu:visible, [role=menu]:visible").get_by_text("Запустить вручную").first.click()
        for _ in range(120):
            await page.wait_for_timeout(2000)
            if await page.get_by_text("Workflow executed successfully").count():
                break
        await page.wait_for_timeout(2000)
        await shot(page, "09-n8n-zapusk.png")
        await browser.close()


async def stage_terminal() -> None:
    url = (Path.home() / "digest-url.txt").read_text().strip()
    cdp.launch("/private/tmp/student")
    await asyncio.sleep(6)
    ed = cdp.Editor()
    await ed.__aenter__()
    await ed.size(1240, 780)
    await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
    await ed.palette("View: Close All Editors", 1.0)
    await ed.palette("Terminal: Kill All Terminals", 1.5)
    await s11.open_terminal(ed)
    await s11.terminal(ed, "clear", 0.5)
    await s11.terminal(ed, f"URL={url}", 0.5)
    await s11.terminal(ed, 'curl -sL "$URL" | head -c 400; echo', 8)
    await s11.terminal(ed, """curl -sL -H "Content-Type: application/json" -d '{"key":"неверный","news":[]}' "$URL"; echo""", 8)
    await s33.term(ed, "07-curl.png")
    await ed.__aexit__(None, None, None)


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    asyncio.run({"google": stage_google, "n8n": stage_n8n, "terminal": stage_terminal}[sys.argv[1]]())
