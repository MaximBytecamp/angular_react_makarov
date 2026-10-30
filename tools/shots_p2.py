"""Кадры страницы «Проект модуля 2»: пример варианта «Общежитие» на PocketBase.

Пример собран из tools/proekt2-obshchezhitie поверх проекта после главы 2.5 и запущен
на порту 5173 (react-kurs/zayavki-obshchezhitie). Коллекция obshchezhitie создана с правилами
главы 2.2 и пятью заявками варианта П1.

    python3 tools/shots_p2.py
"""
import asyncio
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from shots_22 import EMAIL, PASSWORD, PB  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/29-proekt-doska-s-bazoy/img"
URL = "http://localhost:5173/"
FONT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)


async def list_part(page, path: Path, height: int) -> Image.Image:
    box = await page.locator("section.list").bounding_box()
    view = page.viewport_size
    await page.screenshot(path=str(path), clip={"x": box["x"], "y": box["y"], "width": box["width"],
                                                 "height": min(box["height"], view["height"] - box["y"])})
    im = Image.open(path)
    path.unlink()
    return im.crop((0, 0, im.width, min(im.height, height)))


async def main() -> None:
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1100, "height": 900}, device_scale_factor=2)
        one = await ctx.new_page()
        two = await ctx.new_page()
        for pg in (one, two):
            await pg.goto(URL)
            await pg.wait_for_timeout(1500)
        await one.screenshot(path=str(IMG / "01-obshchezhitie.png"), full_page=True)

        await one.locator("#title").press_sequentially("Не закрывается окно", delay=10)
        await one.locator("#room").press_sequentially("215", delay=10)
        await one.locator("#category").select_option("Мебель")
        await one.get_by_role("button", name="Отправить заявку").click()
        await one.wait_for_timeout(2000)
        tmp = IMG / "_tmp.png"
        a = await list_part(one, tmp, 1250)
        c = await list_part(two, tmp, 1250)
        gap, bar = 40, 70
        out = Image.new("RGB", (a.width + c.width + gap * 3, max(a.height, c.height) + bar + gap), "#e3e6ec")
        draw = ImageDraw.Draw(out)
        for x, im, text in ((gap, a, "Окно 1: заявку добавили здесь"), (gap * 2 + a.width, c, "Окно 2: заявка появилась сама")):
            draw.text((x + 6, 18), text, fill="#161A2E", font=FONT)
            out.paste(im, (x, bar))
        out.save(IMG / "02-dva-okna.png")

        pb = await ctx.new_page()
        await pb.set_viewport_size({"width": 1280, "height": 800})
        await pb.goto(f"{PB}/_/")
        await pb.wait_for_timeout(2500)
        await pb.locator("input[type=email]").fill(EMAIL)
        await pb.locator("input[type=password]").fill(PASSWORD)
        await pb.keyboard.press("Enter")
        await pb.wait_for_timeout(2500)
        await pb.goto(f"{PB}/_/#/collections?collection=obshchezhitie")
        await pb.wait_for_timeout(2500)
        await pb.screenshot(path=str(IMG / "03-kollekciya.png"))
        await b.close()
    for p in sorted(IMG.glob("0*.png")):
        print(f"  ✓ {p.name}: {Image.open(p).size}")


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    asyncio.run(main())
