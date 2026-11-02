"""Кадры главы 3.3: сборка приложения «Мониторинг сайтов группы» и публикация на GitHub Pages.

Стадии:
    local   — проект monitoring рядом с react-kurs: создание, разработка, сборка, dist, file://, preview;
    github  — репозиторий MaximBytecamp/monitoring, Pages, три публикации (без base, с base, с BASE_URL).
              Страницы GitHub снимаются в Chrome с профилем ~/repo-shots-chrome на порту 9381 (gh33.mjs).

    python3 tools/shots_33.py local
"""
import asyncio
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import addrbar  # noqa: E402
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_14 as s14  # noqa: E402
from shots_13 import go_line  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/33-github-pages/img/raw"
CODE = Path(__file__).parent / "code33"
PROJECT = s11.WORK.parent / "monitoring"
SRC = PROJECT / "src"


async def code(ed: cdp.Editor, rel: str, line: int, name: str) -> None:
    await s11.open_file(ed, rel)
    await ed.palette("File: Revert File", 1.0)
    await ed.palette("File: Reveal Active File in Explorer View", 1.0)
    await go_line(ed, line)
    await ed.shot(str(IMG / name))


async def term(ed: cdp.Editor, name: str, share_wait: float = 1.5) -> None:
    await ed.palette("View: Toggle Maximized Panel", share_wait)
    await ed.shot(str(IMG / name))
    await ed.palette("View: Toggle Maximized Panel", 1.0)


class Page:
    """Headless Chromium 1100×700 с адресной строкой над кадром и (по желанию) консолью DevTools."""

    async def start(self) -> None:
        from playwright.async_api import async_playwright
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(
            channel="chromium", args=["--remote-debugging-port=9472", "--remote-allow-origins=*"])
        self.ctx = await self.browser.new_context(viewport={"width": 1100, "height": 700}, device_scale_factor=2)
        self.page = await self.ctx.new_page()
        self.dt = None

    async def go(self, url: str) -> None:
        await self.page.goto(url)
        await self.page.wait_for_timeout(2000)

    async def devtools(self, prefix: str) -> None:
        import json
        import urllib.request
        targets = json.loads(urllib.request.urlopen("http://127.0.0.1:9472/json").read())
        tid = next(t["id"] for t in targets if t["url"].startswith(prefix))
        self.dt = await self.ctx.new_page()
        await self.dt.add_init_script("localStorage.setItem('screencast-enabled', 'false')")
        await self.dt.set_viewport_size({"width": 1100, "height": 250})
        await self.dt.goto(f"http://127.0.0.1:9472/devtools/inspector.html?ws=127.0.0.1:9472/devtools/page/{tid}")
        await self.dt.wait_for_timeout(3000)
        try:
            await self.dt.get_by_text("Don't show again").click(timeout=2000)
        except Exception:
            pass
        await self.dt.get_by_role("tab", name="Console").click()
        await self.dt.wait_for_timeout(800)

    async def shot(self, name: str, console: bool = False) -> None:
        from PIL import Image
        path = IMG / name
        await self.page.wait_for_timeout(800)
        await self.page.screenshot(path=str(path))
        if console:
            await self.dt.wait_for_timeout(800)
            tmp = path.with_suffix(".dt.png")
            await self.dt.screenshot(path=str(tmp))
            top, bottom = Image.open(path), Image.open(tmp)
            top = top.crop((0, 0, top.width, int(top.height * 0.74)))
            out = Image.new("RGB", (top.width, top.height + 4 + bottom.height), "#c4c7cf")
            out.paste(top, (0, 0))
            out.paste(bottom, (0, top.height + 4))
            out.save(path)
            tmp.unlink()
        addrbar.add(path, self.page.url)
        print(f"  ✓ {path}")

    async def close(self) -> None:
        await self.browser.close()
        await self.pw.stop()


def put(name: str, dest: str) -> None:
    (PROJECT / dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(CODE / name, PROJECT / dest)


async def stage_local() -> None:
    shutil.rmtree(PROJECT, ignore_errors=True)
    # Создание проекта: терминал VS Code в папке react-kurs, переход на уровень выше.
    cdp.launch(str(s11.WORK))
    await asyncio.sleep(4)
    async with cdp.Editor() as ed:
        await ed.size(1240, 780)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await ed.palette("View: Close All Editors", 1.0)
        await ed.palette("View: Collapse Folders in Explorer", 1.0)
        await s11.open_terminal(ed)
        await s11.terminal(ed, "cd ..", 1)
        await s11.terminal(ed, "npx create-vite@9.2.1 monitoring --template react-ts --no-interactive --no-immediate", 15)
        await term(ed, "01-create-vite.png")

    # Окно VS Code с папкой monitoring.
    cdp.launch(str(PROJECT))
    await asyncio.sleep(5)
    async with cdp.Editor() as ed:
        await ed.size(1240, 780)
        await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
        await ed.palette("View: Show Explorer", 1.2)
        await s11.open_terminal(ed)
        await s11.terminal(ed, "npm install", 12)
        await term(ed, "02-npm-install.png")
        await ed.palette("View: Close Panel", 1)
        await code(ed, "src/App.tsx", 1, "02a-novyy-proekt.png")
        (SRC / "App.css").unlink()
        shutil.rmtree(SRC / "assets")
        put("index.css", "src/index.css")
        put("types.ts", "src/types.ts")
        put("sites.json", "public/data/sites.json")
        put("index.html", "index.html")
        put("App-1.tsx", "src/App.tsx")
        await code(ed, "public/data/sites.json", 1, "03-sites-json.png")
        await code(ed, "src/App.tsx", 12, "04-app.png")
        await ed.palette("View: Close All Editors", 1.0)
        await s11.open_terminal(ed)
        await s11.terminal(ed, "npm run dev", 5)
        await term(ed, "05-dev.png")
        br = Page()
        await br.start()
        await br.go("http://localhost:5173/")
        await br.shot("06-dev-sayt.png")

        # Сборка в dist.
        await s11.open_terminal(ed)
        await s11.terminal(ed, "npm run build", 8)
        await term(ed, "07-build.png")
        await ed.palette("View: Close Panel", 1)
        await code(ed, "dist/index.html", 1, "08-dist.png")
        await br.go(f"file://{PROJECT}/dist/index.html")
        await br.devtools("file://")
        await br.go(f"file://{PROJECT}/dist/index.html")
        await br.shot("09-file.png", console=True)
        await br.dt.close()
        br.dt = None
        await s11.open_terminal(ed)
        await s11.terminal(ed, "npm run preview", 5)
        await term(ed, "10-preview.png")
        await br.go("http://localhost:4173/")
        await br.shot("11-preview-sayt.png")
        await br.close()
        await ed.palette("View: Close Panel", 1)


async def editor() -> cdp.Editor:
    cdp.launch(str(PROJECT))
    await asyncio.sleep(5)
    ed = cdp.Editor()
    await ed.__aenter__()
    await ed.size(1240, 780)
    await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
    await ed.palette("View: Close All Editors", 1.0)
    await ed.palette("View: Close Panel", 1.0)
    await ed.palette("View: Show Explorer", 1.2)
    return ed


async def git_push(ed: cdp.Editor, message: str, name: str, first: bool = False) -> None:
    await s11.open_terminal(ed)
    await ed.palette("Terminal: Clear", 0.8)
    if first:
        await s11.terminal(ed, "git init", 1.5)
    await s11.terminal(ed, "git add .", 1.5)
    await s11.terminal(ed, f'git commit -m "{message}"', 2)
    if first:
        await s11.terminal(ed, "git branch -M main", 1)
        await s11.terminal(ed, "git remote add origin https://github.com/MaximBytecamp/monitoring.git", 1)
        await s11.terminal(ed, "git push -u origin main", 8)
    else:
        await s11.terminal(ed, "git push", 8)
    await term(ed, name)
    await ed.palette("Terminal: Kill the Active Terminal Instance", 1.0)
    await ed.palette("View: Close Panel", 1)


async def stage_push() -> None:
    ed = await editor()
    await git_push(ed, "Список сайтов группы", "14-push.png", first=True)
    await ed.__aexit__(None, None, None)


def wait_run() -> None:
    """Ждёт завершения последнего запуска Actions в репозитории monitoring."""
    import json
    import subprocess
    import time
    time.sleep(8)
    for _ in range(60):
        out = subprocess.run(["gh", "run", "list", "-R", "MaximBytecamp/monitoring", "--limit", "1",
                              "--json", "status,conclusion,databaseId"], capture_output=True, text=True).stdout
        run = json.loads(out)[0]
        if run["status"] == "completed":
            print("  запуск", run["databaseId"], run["conclusion"])
            return
        time.sleep(5)
    raise SystemExit("запуск не завершился")


def gh(stage: str, name: str = "") -> None:
    import subprocess
    subprocess.run([f"{cdp.NODE_BIN}/node", str(Path(__file__).parent / "gh33.mjs"), stage, name], check=True)


async def site(name: str) -> None:
    """Опубликованный сайт с консолью; кэш браузера не используется — новый контекст на каждый кадр."""
    br = Page()
    await br.start()
    await br.go("https://maximbytecamp.github.io/monitoring/")
    await br.devtools("https://maximbytecamp.github.io/monitoring/")
    await br.go("https://maximbytecamp.github.io/monitoring/")
    await br.shot(name, console=True)
    await br.close()


async def stage_deploy() -> None:
    ed = await editor()
    put("deploy.yml", ".github/workflows/deploy.yml")
    await code(ed, ".github/workflows/deploy.yml", 1, "19-deploy-yml.png")
    await ed.palette("View: Close All Editors", 1.0)
    await git_push(ed, "Публикация на GitHub Pages", "20-push-deploy.png")
    await ed.__aexit__(None, None, None)
    wait_run()
    gh("actions", "21")
    await asyncio.sleep(20)
    await site("23-pages-pusto.png")


async def stage_base() -> None:
    ed = await editor()
    put("vite.config.ts", "vite.config.ts")
    await code(ed, "vite.config.ts", 7, "24-vite-base.png")
    await ed.palette("View: Close All Editors", 1.0)
    await git_push(ed, "Адрес сайта в подпапке monitoring", "25-push-base.png")
    await ed.__aexit__(None, None, None)
    wait_run()
    await asyncio.sleep(20)
    await site("26-pages-oshibka-dannyh.png")


async def stage_url() -> None:
    ed = await editor()
    put("App.tsx", "src/App.tsx")
    await code(ed, "src/App.tsx", 12, "27-app-base-url.png")
    await ed.palette("View: Close All Editors", 1.0)
    await git_push(ed, "Путь к sites.json от BASE_URL", "28-push-url.png")
    await ed.__aexit__(None, None, None)
    wait_run()
    gh("actions", "29")
    await asyncio.sleep(20)
    await site("30-pages-rabotaet.png")


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    stages = {"local": stage_local, "push": stage_push, "deploy": stage_deploy, "base": stage_base, "url": stage_url}
    if len(sys.argv) != 2 or sys.argv[1] not in stages:
        raise SystemExit("стадии: " + ", ".join(stages))
    asyncio.run(stages[sys.argv[1]]())
