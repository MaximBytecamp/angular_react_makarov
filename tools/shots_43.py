"""Кадры главы 4.3: задача для ИИ-агента (Continue + Ollama) на «Мониторинге сайтов группы».

Отдельный профиль VS Code /private/tmp/vsc-agent с расширением Continue 2.0.0 (порт отладки 9363),
настройки Continue — в CONTINUE_GLOBAL_DIR=/private/tmp/vsc-agent/continue. Проект — копия
/private/tmp/student43/monitoring (после главы 4.2, закоммичено). Ollama 0.40.16 запущена из
/private/tmp/ollama-mac с моделью qwen3:4b-instruct. Разговоры агента — настоящие прогоны, открываются
из истории Continue по названиям: «Поиск и флажок · задача целиком», «Шаг 1 · поиск», «Возврат с замечаниями».
Панель Continue — webview в отдельном процессе; её элементы нажимаются через webview.py (сырой CDP).

    python3 tools/shots_43.py all
"""
import asyncio
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ["CONTINUE_GLOBAL_DIR"] = "/private/tmp/vsc-agent/continue"
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402
import shots_33 as s33  # noqa: E402
import webview  # noqa: E402

cdp.PROFILE = "/private/tmp/vsc-agent"
cdp.PORT = 9363
webview.PORT = 9363
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/43-zadacha-agentu/img/raw"
s33.IMG = IMG
CODE = Path(__file__).parent / "code43"
C42 = Path(__file__).parent / "code42"
PROJECT = Path("/private/tmp/student43/monitoring")


def put(name: str, dest: str, src: Path = CODE) -> None:
    shutil.copy(src / name, PROJECT / dest)


def reset() -> None:
    """Проект после главы 4.2 (последний коммит) и AGENTS.md."""
    subprocess.run(["git", "checkout", "-q", "--", "."], cwd=PROJECT, check=True)
    subprocess.run(["git", "clean", "-qfd", "src"], cwd=PROJECT, check=True)
    (PROJECT / "ai-log.md").unlink(missing_ok=True)
    put("AGENTS.md", "AGENTS.md")


async def wjs(code: str):
    async with webview.Webview() as w:
        return await w.js(code)


async def panel_task(path: Path) -> None:
    """Вставляет текст задания в поле Continue (событие paste сохраняет переносы строк)."""
    text = json.dumps(path.read_text().strip())
    await wjs("""(async () => {
      const ed = document.querySelector('[contenteditable=true]'); ed.focus();
      const dt = new DataTransfer(); dt.setData('text/plain', %s);
      ed.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
      await new Promise(r => setTimeout(r, 800)); })()""" % text)


async def agent_mode(open_menu: bool = False) -> None:
    await wjs("""(async () => {
      document.querySelector('[data-testid=mode-select-button]').click();
      await new Promise(r => setTimeout(r, 600));
      const a = [...document.querySelectorAll('[role=option]')].find(e => e.innerText.startsWith('Agent'));
      if (!%s) a.click(); })()""" % ("true" if open_menu else "false"))


async def open_session(ed: cdp.Editor, title: str) -> None:
    await ed.palette("Continue: View History", 2.0)
    await wjs("""(async () => {
      const row = [...document.querySelectorAll('[data-testid^=history-row]')].find(r => r.innerText.includes(%s));
      row.click(); await new Promise(r => setTimeout(r, 1500));
      const box = [...document.querySelectorAll('*')].find(e => e.scrollHeight > e.clientHeight + 50 && getComputedStyle(e).overflowY !== 'visible');
      if (box) box.scrollTop = box.scrollHeight; })()""" % json.dumps(title))
    await asyncio.sleep(1.5)


async def close_error_card() -> None:
    await wjs("""(() => { const t = document.querySelector('[data-testid=error-output-toggle]');
      if (t) { const card = t.closest('div.rounded-lg, div[class*=shadow]') || t.parentElement.parentElement;
        const x = card.querySelector('button'); if (x) x.click(); } })()""")


async def editor() -> cdp.Editor:
    cdp.launch(str(PROJECT))
    await asyncio.sleep(8)
    ed = cdp.Editor()
    await ed.__aenter__()
    await ed.size(1240, 780)
    await ed.send("Emulation.setFocusEmulationEnabled", enabled=True)
    await ed.palette("View: Close All Editors", 1.0)
    await ed.palette("View: Close Panel", 1.0)
    return ed


async def sidebar(ed: cdp.Editor, width: int) -> None:
    """Ширина боковой панели перетаскиванием её границы: панель Continue — около 550 точек, проводник — 240."""
    import json as _json
    b = _json.loads(await ed.js("JSON.stringify(document.querySelector('.part.sidebar').getBoundingClientRect())"))
    x0, x1, y = b["right"] + 1, b["left"] + width, 400
    await ed.send("Input.dispatchMouseEvent", type="mousePressed", x=x0, y=y, button="left", clickCount=1)
    for i in range(1, 11):
        await ed.send("Input.dispatchMouseEvent", type="mouseMoved", x=x0 + (x1 - x0) * i / 10, y=y, button="left", buttons=1)
        await asyncio.sleep(0.05)
    await ed.send("Input.dispatchMouseEvent", type="mouseReleased", x=x1, y=y, button="left", clickCount=1)
    await asyncio.sleep(0.8)


async def wide_panel(ed: cdp.Editor) -> None:
    await ed.palette("Continue: Focus on Continue Input", 2.0)
    await sidebar(ed, 550)


async def narrow(ed: cdp.Editor) -> None:
    await ed.palette("View: Show Explorer", 1.0)
    await sidebar(ed, 240)


async def term(ed: cdp.Editor, command: str, name: str, wait: float) -> None:
    await ed.palette("Terminal: Kill All Terminals", 1.5)
    await s11.open_terminal(ed)
    await s11.terminal(ed, command, wait)
    await s33.term(ed, name)
    await ed.palette("View: Close Panel", 1)


def dev_server() -> subprocess.Popen:
    env = {"PATH": f"{cdp.NODE_BIN}:/usr/bin:/bin"}
    proc = subprocess.Popen([f"{cdp.NODE_BIN}/npx", "vite", "--port", "5173", "--strictPort"], cwd=PROJECT,
                            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import time
    for _ in range(30):
        try:
            urllib.request.urlopen("http://localhost:5173/monitoring/")
            return proc
        except OSError:
            time.sleep(0.5)
    raise SystemExit("vite не запустился")


async def stage_all() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    reset()
    ed = await editor()

    # §2–3. Ollama, Continue, настройки.
    await term(ed, "ollama list", "01-ollama-list.png", 3)
    await ed.palette("Extensions: Show Installed Extensions", 3.0)
    await ed.shot(str(IMG / "02-continue-extension.png"))
    await ed.palette("View: Toggle Breadcrumbs", 0.8)
    await s33.code(ed, "/private/tmp/vsc-agent/continue/config.yaml", 1, "03-config-yaml.png")
    await ed.palette("View: Toggle Breadcrumbs", 0.8)
    await ed.palette("View: Close All Editors", 1.0)
    await wide_panel(ed)
    await ed.palette("Continue: New Session", 2.0)
    await close_error_card()
    await agent_mode(open_menu=True)
    await asyncio.sleep(1)
    await ed.shot(str(IMG / "04-agent-mode.png"))
    await ed.key("Escape", 0.5)
    await agent_mode()

    # §4–5. AGENTS.md, задание, ответ на задачу целиком.
    await narrow(ed)
    await s33.code(ed, "AGENTS.md", 1, "05-agents-md.png")
    await ed.palette("View: Close All Editors", 1.0)
    await wide_panel(ed)
    await panel_task(CODE / "zadanie.md")
    await ed.shot(str(IMG / "06-zadanie.png"))
    await open_session(ed, "Поиск и флажок · задача целиком")
    await ed.shot(str(IMG / "07-otvet-celikom.png"))

    # §6. Шаг 1: живой прогон до правки, ждущей подтверждения.
    await ed.palette("Continue: New Session", 2.0)
    await agent_mode()
    await panel_task(CODE / "shag1.md")
    await wjs("document.querySelector('[data-testid=submit-input-button]').click()")
    for _ in range(90):
        await asyncio.sleep(5)
        if await wjs("!!document.querySelector('[data-testid=edit-accept-button]')"):
            break
    await asyncio.sleep(3)
    await ed.shot(str(IMG / "08-pravka.png"))
    await wjs("document.querySelectorAll('[data-testid=edit-reject-button]').forEach(b => b.click())")
    await asyncio.sleep(2)
    await wjs("(() => { const s = [...document.querySelectorAll('button')].find(b => (b.innerText||'').startsWith('Stop')); if (s) s.click(); })()")
    await asyncio.sleep(2)
    await ed.palette("View: Close All Editors", 1.0)
    await open_session(ed, "Шаг 1 · поиск")
    await ed.shot(str(IMG / "09-komandy.png"))

    # Проверка кода агента после шага 1.
    reset()
    put("SitesPage-agent.tsx", "src/pages/SitesPage.tsx")
    put("SitesPage.test.tsx", "src/pages/SitesPage.test.tsx", C42)
    await narrow(ed)
    await term(ed, "npx tsc -b", "10-tsc.png", 6)
    await term(ed, "npm run lint -- --deny-warnings", "11-lint.png", 3)
    await term(ed, "CI=true npm test", "12-testy.png", 8)
    await ed.palette("Git: Refresh", 2.0)
    await ed.palette("View: Show Source Control", 2.0)
    xy = await ed.js("(() => { const r = [...document.querySelectorAll('.scm-view .monaco-list-row')].find(r => /^SitesPage\\.tsx/.test(r.getAttribute('aria-label') || '')); const b = r.getBoundingClientRect(); return JSON.stringify([b.x + 60, b.y + b.height / 2]); })()")
    xy = json.loads(xy)
    await ed.click(xy[0], xy[1], 2.5)
    await ed.palette("View: Close Primary Side Bar", 1.0)
    await ed.shot(str(IMG / "13-diff.png"))
    await ed.palette("View: Close All Editors", 1.0)

    # §7. Возврат и решение.
    await wide_panel(ed)
    await open_session(ed, "Возврат с замечаниями")
    await ed.shot(str(IMG / "14-vozvrat.png"))
    reset()
    for name, dest in (("SitesPage.tsx", "src/pages/SitesPage.tsx"), ("SitesPage.test.tsx", "src/pages/SitesPage.test.tsx"),
                       ("index.css", "src/index.css")):
        put(name, dest)
    await narrow(ed)
    await s33.code(ed, "src/pages/SitesPage.tsx", 36, "15-sitespage.png")
    await ed.palette("View: Close All Editors", 1.0)
    await term(ed, "npx tsc -b && npm run lint -- --deny-warnings && CI=true npm test", "16-vse-zeleno.png", 12)

    server = dev_server()
    br = s33.Page()
    await br.start()
    await br.go("http://localhost:5173/monitoring/")
    for _ in range(4):
        await br.page.keyboard.press("Tab")
    await br.page.keyboard.press("Space")
    await br.shot("17-stranica.png")
    await br.close()
    server.terminate()

    # §8. Журнал.
    put("ai-log.md", "ai-log.md")
    await s33.code(ed, "ai-log.md", 1, "18-ai-log.png")
    await ed.__aexit__(None, None, None)


async def stage_log() -> None:
    """Только кадр журнала: после правки ai-log.md."""
    put("ai-log.md", "ai-log.md")
    ed = await editor()
    await narrow(ed)
    await s33.code(ed, "ai-log.md", 1, "18-ai-log.png")
    await ed.__aexit__(None, None, None)


if __name__ == "__main__":
    asyncio.run({"all": stage_all, "log": stage_log}[sys.argv[1]]())
