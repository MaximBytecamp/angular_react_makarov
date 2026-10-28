"""Кадры главы 1.5: списки, ключи, условный вывод.

Продолжает проект zayavki после главы 1.4. Код — из tools/code15. Браузер и консоль —
как в tools/shots_14.py (headless Chromium с портом 9471), окно страницы выше:
в списке пять заявок.

    python3 tools/shots_15.py reset   # проект в состоянии конца главы 1.4
    python3 tools/shots_15.py all
"""
import asyncio
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_14 as s14  # noqa: E402
from shots_13 import go_line  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/15-spiski-i-usloviya/img/raw"
C14 = Path(__file__).parent / "code14"
CODE = Path(__file__).parent / "code15"
SRC = s11.PROJECT / "src"


def reset() -> None:
    """Состояние конца главы 1.4."""
    s14.reset()
    for name in ("App.tsx", "index.css"):
        shutil.copy(C14 / name, SRC / name)
    for name in ("Header.tsx", "RequestCard.tsx"):
        shutil.copy(C14 / name, SRC / "components" / name)
    (SRC / "requests.ts").unlink(missing_ok=True)
    print("проект в состоянии конца главы 1.4")


def put(src_name: str, dest: str) -> None:
    shutil.copy(CODE / src_name, SRC / dest)


class Browser(s14.Browser):
    """Окно 1100×900: пять карточек видны целиком."""

    async def start(self) -> None:
        await super().start()
        await self.page.set_viewport_size({"width": 1100, "height": 900})

    async def full(self, path: Path) -> None:
        # Открытая DevTools рисует ярлык с размером окна, когда снимок всей страницы меняет его высоту.
        if self.dt is not None:
            await self.dt.close()
            self.dt = None
        await self.page.wait_for_timeout(800)
        await self.page.screenshot(path=str(path), full_page=True)
        print(f"  ✓ {path}")


async def lint(ed: cdp.Editor, path: Path) -> None:
    await s11.open_terminal(ed)
    await s11.terminal(ed, "cd zayavki && npm run lint", 5)
    await ed.palette("View: Toggle Maximized Panel", 1.5)
    await ed.shot(str(path))
    await ed.palette("View: Toggle Maximized Panel", 1.0)
    await ed.palette("Terminal: Kill the Active Terminal Instance", 1.0)
    await ed.palette("View: Close Panel", 1)


async def all_frames() -> None:
    reset()
    cdp.launch(str(s11.WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1240, 780)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd zayavki && npm run dev", 6)
        await ed.palette("View: Close Panel", 1)
        await ed.palette("View: Show Explorer", 1.2)
        br = Browser()
        await br.start()

        # §1. Файл с массивом заявок.
        put("requests.ts", "requests.ts")
        await s14.reveal(ed, "zayavki/src/requests.ts")
        await ed.palette("File: Reveal Active File in Explorer View", 1.0)
        await go_line(ed, 1)
        await ed.shot(str(IMG / "01-requests-ts.png"))

        # §2. map без ключа: список на странице и предупреждение в консоли.
        put("RequestCard-import.tsx", "components/RequestCard.tsx")
        put("App-bez-key.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "02-app-map.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.full(IMG / "03-spisok-pyat.png")
        await br.devtools()
        await br.load()
        await br.shot(IMG / "04-konsol-key.png", console=True)
        await lint(ed, IMG / "05-lint-key.png")

        put("App-map.tsx", "App.tsx")
        await asyncio.sleep(1.5)
        await br.devtools()
        await br.load()
        await br.shot(IMG / "06-konsol-chisto.png", console=True)

        # §3. Изменение массива напрямую: в консоли новый статус, на странице старый.
        put("App-mutaciya.tsx", "App.tsx")
        await asyncio.sleep(1.5)
        await br.devtools()
        await br.load()
        await br.click("Взять в работу", 0)
        await br.shot(IMG / "07-mutaciya.png", console=True)
        await lint(ed, IMG / "08-lint-mutaciya.png")

        # Новый массив через map: статус и счётчик меняются.
        put("App-map.tsx", "App.tsx")
        await asyncio.sleep(1.5)
        await br.load()
        await br.click("Взять в работу", 0)
        await br.full(IMG / "09-map-novyy-massiv.png")

        # §4. Условный вывод в карточке, удаление заявки.
        put("index-uslovie.css", "index.css")
        put("RequestCard.tsx", "components/RequestCard.tsx")
        put("App-uslovie.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/components/RequestCard.tsx")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "10-card-uslovie.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.full(IMG / "11-svernuto.png")
        await br.click("Подробнее", 0)
        await br.full(IMG / "12-podrobnee.png")
        await br.click("Убрать с доски", 0)
        await br.full(IMG / "13-ubrana.png")

        # §5. Фильтр по статусу.
        put("index.css", "index.css")
        put("App.tsx", "App.tsx")
        await s14.reveal(ed, "zayavki/src/App.tsx")
        await go_line(ed, 1)
        await ed.shot(str(IMG / "14-app-filtr.png"))
        await asyncio.sleep(1.5)
        await br.load()
        await br.full(IMG / "15-filtr-vse.png")
        await br.page.locator(".filters button", has_text="Новая").click()
        await br.full(IMG / "16-filtr-novaya.png")
        await br.page.locator(".filters button", has_text="Все").click()
        await br.click("Убрать с доски", 0)
        await br.page.locator(".filters button", has_text="Готово").click()
        await br.full(IMG / "17-filtr-pusto.png")

        # §6. Ключ — номер в массиве: раскрытая карточка «переезжает».
        put("App-index.tsx", "App.tsx")
        await asyncio.sleep(1.5)
        for name, prefix in (("index", "18-index"), ("id", "20-id")):
            if name == "id":
                put("App.tsx", "App.tsx")
                await asyncio.sleep(1.5)
            await br.load()
            await br.click("Подробнее", 3)
            await br.full(IMG / f"{prefix}-do.png")
            await br.click("Убрать с доски", 0)
            await br.full(IMG / f"{prefix.replace('18', '19').replace('20', '21')}-posle.png")
        await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name == "reset":
        reset()
    elif name == "all":
        asyncio.run(all_frames())
    else:
        raise SystemExit("стадии: reset, all")
