"""Кадры главы 1.1: Node.js, npm и проект на Vite.

Всё снимается в фоне: отдельный экземпляр VS Code управляется по протоколу
DevTools (tools/cdp.py), страницы в браузере — headless Chromium из Playwright.
Экран пользователя не переключается.

    python3 tools/shots_11.py setup      # профиль редактора и пустая папка студента
    python3 tools/shots_11.py <стадия>   # одна стадия; список — STAGES внизу

Папка студента — /private/tmp/student/react-kurs, проект создаётся в ней командой
из главы. Node 24 LTS берётся из /private/tmp/node24 (см. cdp.NODE_BIN).
"""
import asyncio
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
# Съёмка пишет исходные кадры в img/raw; tools/crop_11.py кладёт обрезанные в img/.
IMG = ROOT / "temy/11-node-npm-vite/img/raw"
WORK = Path("/private/tmp/student/react-kurs")
PROJECT = WORK / "zayavki"

SETTINGS = {
    "workbench.colorTheme": "Default Light Modern",
    "security.workspace.trust.enabled": False,
    "workbench.startupEditor": "none",
    "workbench.tips.enabled": False,
    "workbench.secondarySideBar.defaultVisibility": "hidden",
    "chat.disableAIFeatures": True,
    "chat.commandCenter.enabled": False,
    "window.commandCenter": False,
    "editor.minimap.enabled": False,
    "editor.fontSize": 14,
    "terminal.integrated.fontSize": 14,
    "terminal.integrated.defaultProfile.osx": "bash",
    "terminal.integrated.profiles.osx": {
        "bash": {"path": "/bin/bash", "args": ["--norc", "--noprofile"]},
    },
    "terminal.integrated.env.osx": {"PS1": "\\W $ ", "BASH_SILENCE_DEPRECATION_WARNING": "1",
                                    "PATH": cdp.NODE_BIN + ":/usr/bin:/bin:/usr/sbin:/sbin",
                                    # Пустой кэш npm: студент на первом запуске видит вопрос «Ok to proceed?».
                                    "npm_config_cache": "/private/tmp/student/npm-cache",
                                    "npm_config_update_notifier": "false",
                                    "npm_config_fund": "false"},
    "terminal.integrated.showExitAlert": False,
    "telemetry.telemetryLevel": "off",
    "update.mode": "none",
    "extensions.ignoreRecommendations": True,
    "git.openRepositoryInParentFolders": "never",
    "explorer.compactFolders": False,
}


def setup() -> None:
    """Чистый профиль и пустая папка студента."""
    subprocess.run(["pkill", "-9", "-f", f"user-data-dir={cdp.PROFILE}/data"], capture_output=True)
    shutil.rmtree(cdp.PROFILE, ignore_errors=True)
    user = Path(cdp.PROFILE) / "data/User"
    user.mkdir(parents=True)
    (Path(cdp.PROFILE) / "ext").mkdir()
    (user / "settings.json").write_text(json.dumps(SETTINGS, ensure_ascii=False, indent=2))
    shutil.rmtree(WORK.parent, ignore_errors=True)
    WORK.mkdir(parents=True)
    IMG.mkdir(parents=True, exist_ok=True)
    print("профиль и папка готовы")


async def terminal(ed: cdp.Editor, command: str, wait: float) -> None:
    """Набирает команду в открытом терминале и ждёт результата."""
    await ed.paste(command, 0.3)
    await ed.key("Enter", wait)


async def open_terminal(ed: cdp.Editor) -> None:
    await ed.palette("Terminal: Create New Terminal", 2.5)


async def stage_versions() -> None:
    """Окно с пустой папкой, терминал: node -v и npm -v."""
    cdp.launch(str(WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1100, 420)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await ed.palette("View: Close Primary Side Bar", 1)
        await open_terminal(ed)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await terminal(ed, "node -v", 1.5)
        await terminal(ed, "npm -v", 2.5)
        await ed.shot(str(IMG / "01-node-npm-versii.png"))


async def browser_shot(path: Path, url: str = "http://localhost:5173/", page=None):
    """Снимок страницы в headless Chromium; страница остаётся открытой для следующего кадра."""
    from playwright.async_api import async_playwright
    if page is None:
        pw = await async_playwright().start()
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1100, "height": 700}, device_scale_factor=2)
        await page.goto(url)
    await page.wait_for_timeout(1500)
    await page.screenshot(path=str(path))
    print(f"  ✓ {path}")
    return page


async def stage_project() -> None:
    """Создание проекта, установка, запуск, страница, проводник, живое обновление."""
    cdp.launch(str(WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1100, 560)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await ed.palette("View: Close Primary Side Bar", 1)
        await open_terminal(ed)
        await ed.palette("View: Toggle Maximized Panel", 1.5)
        await terminal(ed, "npm create vite@latest zayavki -- --template react-ts", 12)
        await ed.shot(str(IMG / "02-create-ok-to-proceed.png"))
        await terminal(ed, "y", 10)
        await ed.shot(str(IMG / "03-create-linter.png"))
        await ed.key("Enter", 3)
        await ed.shot(str(IMG / "04-create-install-now.png"))
        await ed.key("ArrowRight", 0.8)
        await ed.key("Enter", 4)
        await ed.shot(str(IMG / "05-create-done.png"))
        await terminal(ed, "clear", 0.8)
        await terminal(ed, "cd zayavki", 1)
        await terminal(ed, "npm install", 1)
        for _ in range(90):
            if (PROJECT / "node_modules/.package-lock.json").exists():
                break
            await asyncio.sleep(1)
        await asyncio.sleep(4)
        await ed.shot(str(IMG / "06-npm-install.png"))
        await terminal(ed, "clear", 0.8)
        await terminal(ed, "npm run dev", 6)
        await ed.shot(str(IMG / "07-npm-run-dev.png"))

        await browser_shot(IMG / "08-stranica-vite.png")



async def open_file(ed: cdp.Editor, name: str) -> None:
    """Открывает файл через быстрый поиск (⌘P): системное окно «Открыть» по протоколу недоступно."""
    await ed.key("Meta+P", 1.0)
    await ed.paste(name, 1.2)
    await ed.key("Enter", 2.0)


async def stage_explorer() -> None:
    """Проводник с деревом проекта, main.tsx и App.tsx, живое обновление страницы."""
    cdp.launch(str(WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1240, 780)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await open_terminal(ed)
        await terminal(ed, "cd zayavki && npm run dev", 6)
        await ed.palette("View: Close Panel", 1)
        page = await browser_shot(IMG / "08-stranica-vite.png")

        await ed.palette("View: Show Explorer", 1.5)
        await open_file(ed, "zayavki/src/main.tsx")
        await ed.palette("File: Reveal Active File in Explorer View", 1.5)
        await ed.shot(str(IMG / "09-provodnik-main.png"))

        await open_file(ed, "zayavki/src/App.tsx")
        await ed.shot(str(IMG / "10-app-tsx.png"))

        # Живое обновление: счётчик нажат три раза, затем правка заголовка.
        # После правки на счётчике остаётся 3 — страница не перезагружалась.
        for _ in range(3):
            await page.click("button.counter")
        await browser_shot(IMG / "08b-schetchik-3.png", page=page)
        app = PROJECT / "src/App.tsx"
        app.write_text(app.read_text().replace("<h1>Get started</h1>", "<h1>Доска заявок</h1>"))
        await asyncio.sleep(2.5)
        await ed.shot(str(IMG / "11-app-pravka.png"))
        await browser_shot(IMG / "12-stranica-hmr.png", page=page)

        # Заготовка проекта: файлы шаблона заменены, лишнее удалено.
        (PROJECT / "src/App.tsx").write_text(KARKAS_APP)
        (PROJECT / "src/index.css").write_text(KARKAS_CSS)
        (PROJECT / "src/App.css").unlink(missing_ok=True)
        shutil.rmtree(PROJECT / "src/assets", ignore_errors=True)
        await asyncio.sleep(2.5)
        await ed.palette("File: Revert File", 1.5)
        await ed.shot(str(IMG / "13-app-karkas.png"))
        await page.reload()
        await browser_shot(IMG / "14-stranica-karkas.png", page=page)


KARKAS_APP = """function App() {
  return (
    <main>
      <h1>Доска заявок</h1>
      <p>Здесь появятся форма заявки и список карточек.</p>
    </main>
  )
}

export default App
"""

KARKAS_CSS = """:root {
  font-family: system-ui, 'Segoe UI', Roboto, sans-serif;
  color: #1f2430;
  background: #f6f7f9;
}

body {
  margin: 0;
}

main {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 20px;
}
"""


async def stage_nodejs() -> None:
    """Страница загрузки nodejs.org так, как её видит студент на Windows."""
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": 1200, "height": 760}, device_scale_factor=2, locale="ru-RU",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
        page = await ctx.new_page()
        await page.goto("https://nodejs.org/en/download", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(IMG / "00-nodejs-download.png"))
        print(f"  ✓ {IMG / '00-nodejs-download.png'}")
        await browser.close()


STAGES = {"nodejs": stage_nodejs, "versions": stage_versions, "project": stage_project, "explorer": stage_explorer}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name == "setup":
        setup()
    elif name in STAGES:
        asyncio.run(STAGES[name]())
    else:
        raise SystemExit(f"стадии: setup, {', '.join(STAGES)}")
