"""Кадры главы 2.5: обновление списка по событиям PocketBase.

Продолжает проект zayavki после главы 2.4 (tools/code24) и PocketBase с семью заявками
конца главы 2.4. Два окна доски снимаются рядом: из каждого берётся раздел со списком,
над ним — подпись окна.

    python3 tools/shots_25.py all
"""
import asyncio
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_14 as s14  # noqa: E402
import shots_15 as s15  # noqa: E402
import shots_16 as s16  # noqa: E402
import shots_23 as s23  # noqa: E402
from shots_13 import go_line  # noqa: E402
from shots_22 import EMAIL, PASSWORD, PB  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/25-obnovlenie-po-sobytiyam/img/raw"
C23 = Path(__file__).parent / "code23"
C24 = Path(__file__).parent / "code24"
CODE = Path(__file__).parent / "code25"
SRC = s11.PROJECT / "src"
KEEP = s23.SEED + ["Не печатает принтер", "Нет звука в колонках"]
FONT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)


def reset_db() -> None:
    """Семь заявок конца главы 2.4; у «Не работает мышь» категория «Компьютер»."""
    token = s23.api("POST", "/api/collections/_superusers/auth-with-password",
                    body={"identity": EMAIL, "password": PASSWORD})["token"]
    path = "/api/collections/requests/records"
    for item in s23.api("GET", f"{path}?perPage=200", token)["items"]:
        if item["title"] not in KEEP:
            s23.api("DELETE", f"{path}/{item['id']}", token)
        elif item["title"] == "Не работает мышь" and item["category"] != "Компьютер":
            s23.api("PATCH", f"{path}/{item['id']}", token, {"category": "Компьютер"})


def reset() -> None:
    """Проект конца главы 2.4 без библиотеки pocketbase."""
    for name in ("App.tsx", "useRequests.ts"):
        shutil.copy(C24 / name, SRC / name)
    for name in ("api.ts", "requests.ts", "index.css"):
        shutil.copy(C23 / name, SRC / name)
    shutil.copy(Path(__file__).parent / "code14/Header.tsx", SRC / "components/Header.tsx")
    (SRC / "realtime.ts").unlink(missing_ok=True)
    subprocess.run(["npm", "uninstall", "pocketbase"], cwd=s11.PROJECT, capture_output=True,
                   env={"PATH": f"{cdp.NODE_BIN}:/usr/bin:/bin", "HOME": str(Path.home())})


def put(name: str, dest: str) -> None:
    shutil.copy(CODE / name, SRC / dest)


async def list_part(page, path: Path, height: int) -> Image.Image:
    # Снимок в пределах окна: снимок элемента целиком меняет размер окна, и DevTools рисует ярлык размера.
    box = await page.locator("section.list").bounding_box()
    view = page.viewport_size
    await page.screenshot(path=str(path), clip={"x": box["x"], "y": box["y"], "width": box["width"],
                                                 "height": min(box["height"], view["height"] - box["y"])})
    im = Image.open(path)
    path.unlink()
    return im.crop((0, 0, im.width, min(im.height, height)))


async def pair(br: s15.Browser, second, name: str, left: str, right: str, height: int = 1250) -> None:
    """Списки двух окон рядом, над каждым подпись."""
    tmp = IMG / "_tmp.png"
    a = await list_part(br.page, tmp, height)
    b = await list_part(second, tmp, height)
    gap, bar = 40, 70
    out = Image.new("RGB", (a.width + b.width + gap * 3, max(a.height, b.height) + bar + gap), "#e3e6ec")
    draw = ImageDraw.Draw(out)
    for x, im, text in ((gap, a, left), (gap * 2 + a.width, b, right)):
        draw.text((x + 6, 18), text, fill="#161A2E", font=FONT)
        out.paste(im, (x, bar))
    out.save(IMG / name)
    print(f"  ✓ {IMG / name}")


async def both_load(br: s15.Browser, second) -> None:
    await br.load()
    await second.goto(s14.URL)
    await second.wait_for_timeout(1500)


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
        await br.load()
        await br.devtools()
        second = await br.ctx.new_page()
        await second.set_viewport_size({"width": 1100, "height": 900})

        # §1. Без подписки второе окно не видит новую заявку.
        await both_load(br, second)
        await s16.fill(br, "Не работает интерактивная доска", "214", "Компьютер", "")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.page.wait_for_timeout(1500)
        await pair(br, second, "01-dva-okna-do.png", "Окно 1: заявку добавили здесь", "Окно 2: без изменений")

        # §2. Библиотека pocketbase и файл подписки.
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki", 1)
        await s11.terminal(ed, "npm install pocketbase@0.28.1", 12)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await ed.shot(str(IMG / "02-npm-install.png"))
        await ed.palette("View: Toggle Maximized Panel", 1.0)
        await ed.palette("View: Close Panel", 1)
        put("realtime.ts", "realtime.ts")
        await s14.reveal(ed, "zayavki/src/realtime.ts")
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await go_line(ed, 1)
        await ed.shot(str(IMG / "03-realtime-ts.png"))

        # §3. Подписка без проверки повторов.
        put("useRequests-dubli.ts", "useRequests.ts")
        await s14.reveal(ed, "zayavki/src/useRequests.ts")
        await go_line(ed, 36)
        await ed.shot(str(IMG / "04-hook-dubli.png"))
        await asyncio.sleep(1.5)
        await both_load(br, second)
        await br.dt.locator('[aria-label="Clear console"]').first.click()
        await s16.fill(br, "Не открывается журнал", "305", "Интернет", "")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.page.wait_for_timeout(1800)
        await br.shot(IMG / "06-konsol-key.png", console=True)
        await pair(br, second, "05-dva-okna-dubli.png", "Окно 1: заявка дважды", "Окно 2: заявка один раз")

        # §4. upsertRequest: по одной карточке, изменения в обе стороны.
        put("requests.ts", "requests.ts")
        put("useRequests.ts", "useRequests.ts")
        await s14.reveal(ed, "zayavki/src/requests.ts")
        await go_line(ed, 28)
        await ed.shot(str(IMG / "07-requests-upsert.png"))
        await s14.reveal(ed, "zayavki/src/useRequests.ts")
        await go_line(ed, 36)
        await ed.shot(str(IMG / "08-hook-final.png"))
        await asyncio.sleep(1.5)
        await both_load(br, second)
        await s16.fill(br, "Не работает сканер", "112", "Принтер", "")
        await br.page.get_by_role("button", name="Отправить заявку").click()
        await br.page.wait_for_timeout(1800)
        await pair(br, second, "09-dva-okna-dobavlenie.png", "Окно 1: заявку добавили здесь", "Окно 2: заявка появилась сама")
        await second.locator("article.card", has_text="Не работает сканер").get_by_role("button", name="Взять в работу").click()
        await second.wait_for_timeout(1500)
        await pair(br, second, "10-dva-okna-status.png", "Окно 1: статус сменился сам", "Окно 2: нажали «Взять в работу»")

        # Изменение из панели PocketBase.
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
        await pb.get_by_text("Не работает мышь", exact=True).first.click()
        await pb.wait_for_timeout(1200)
        await pb.locator(".record-field-input.field-type-select").first.locator("button.selected-container").click()
        await pb.wait_for_timeout(300)
        await pb.locator(".dropdown-item.select-option", has_text="Интернет").first.click()
        await pb.wait_for_timeout(500)
        await pb.screenshot(path=str(IMG / "11-panel-kategoriya.png"))
        print(f"  ✓ {IMG / '11-panel-kategoriya.png'}")
        await pb.get_by_role("button", name="Save changes").click()
        await pb.wait_for_timeout(1500)
        await br.page.bring_to_front()
        await br.page.wait_for_timeout(500)
        await br.full(IMG / "12-doska-kategoriya.png")

        # §5. Канал событий во вкладке Network.
        await br.devtools()
        await s23.network_tab(br)
        await br.dt.get_by_text("All", exact=True).first.click()
        await br.load()
        await br.page.wait_for_timeout(1500)
        await second.locator("article.card", has_text="Не работает сканер").get_by_role("button", name="Завершить").click()
        await br.page.wait_for_timeout(1500)
        # Первая строка realtime — соединение GET с потоком событий, следующие — POST с подпиской.
        await (await realtime_row(br)).as_element().click()
        await br.dt.wait_for_timeout(800)
        await br.dt.get_by_role("tab", name="EventStream").click()
        await br.dt.wait_for_timeout(800)
        await br.shot(IMG / "13-eventstream.png", console=True)
        await pb.close()
        await br.close()


async def realtime_row(br: s15.Browser):
    """Строка таблицы Network: ячейки лежат в теневом DOM, ищем по тексту обходом дерева."""
    return await br.dt.evaluate_handle("""() => {
      let found = null
      const walk = (n) => {
        if (found) return
        if (n.shadowRoot) walk(n.shadowRoot)
        for (const c of n.children || []) walk(c)
        if (!found && n.matches && n.matches('td.name-column') && n.innerText.trim() === 'realtime') found = n
      }
      walk(document)
      return found
    }""")


async def eventstream() -> None:
    """Только кадр §5: проект и база уже в состоянии конца главы."""
    br = s15.Browser()
    await br.start()
    await br.load()
    # DevTools подключается к первой вкладке с адресом доски, поэтому второе окно — после него.
    await br.devtools()
    second = await br.ctx.new_page()
    await second.set_viewport_size({"width": 1100, "height": 900})
    await second.goto(s14.URL)
    await s23.network_tab(br)
    await br.dt.get_by_text("All", exact=True).first.click()
    await br.load()
    await br.page.wait_for_timeout(1500)
    await second.wait_for_timeout(500)
    await second.get_by_role("button", name="Взять в работу").first.click()
    await br.page.wait_for_timeout(1500)
    await (await realtime_row(br)).as_element().click()
    await br.dt.wait_for_timeout(800)
    await br.dt.get_by_role("tab", name="EventStream").click()
    await br.dt.wait_for_timeout(800)
    await br.shot(IMG / "13-eventstream.png", console=True)
    await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    elif sys.argv[1:] == ["es"]:
        asyncio.run(eventstream())
    else:
        raise SystemExit("стадии: all")
