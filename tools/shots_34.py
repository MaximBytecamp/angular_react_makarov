"""Кадры главы 3.4: ночная проверка сайтов в GitHub Actions для приложения monitoring.

Продолжает проект /private/tmp/student/monitoring и репозиторий MaximBytecamp/monitoring после главы 3.3.
Помощники (окно VS Code, отправка, ожидание запуска, браузер с адресной строкой) — из shots_33.py.
Страницы GitHub снимает gh34.mjs.

    python3 tools/shots_34.py local | perm | publish
"""
import asyncio
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import shots_11 as s11  # noqa: E402
import shots_33 as s33  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/34-github-actions/img/raw"
s33.IMG = IMG
CODE = Path(__file__).parent / "code34"
PROJECT = s33.PROJECT
SITE = "https://maximbytecamp.github.io/monitoring/"


def put(name: str, dest: str) -> None:
    (PROJECT / dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(CODE / name, PROJECT / dest)


def gh(stage: str, *args: str) -> None:
    import subprocess
    subprocess.run([f"{s33.cdp.NODE_BIN}/node", str(Path(__file__).parent / "gh34.mjs"), stage, *args], check=True)


async def git_pull_push(ed, message: str, name: str) -> None:
    """Перед отправкой — git pull: бот добавил в репозиторий коммит с результатами."""
    await s11.open_terminal(ed)
    await ed.palette("Terminal: Clear", 0.8)
    await s11.terminal(ed, "git pull", 4)
    await s11.terminal(ed, "git add .", 1.5)
    await s11.terminal(ed, f'git commit -m "{message}"', 2)
    await s11.terminal(ed, "git push", 8)
    await s33.term(ed, name)
    await ed.palette("Terminal: Kill the Active Terminal Instance", 1.0)
    await ed.palette("View: Close Panel", 1)


async def site(name: str) -> None:
    br = s33.Page()
    await br.start()
    await br.go(SITE)
    await br.shot(name)
    await br.close()


async def stage_local() -> None:
    (PROJECT / "public/data/results.json").unlink(missing_ok=True)
    ed = await s33.editor()
    put("check.mjs", "scripts/check.mjs")
    await s33.code(ed, "scripts/check.mjs", 14, "01-check-mjs.png")
    await ed.palette("View: Close All Editors", 1.0)
    await s11.open_terminal(ed)
    await ed.palette("Terminal: Clear", 0.8)
    await s11.terminal(ed, "node scripts/check.mjs", 10)
    await s33.term(ed, "02-check-zapusk.png")
    await ed.palette("View: Close Panel", 1)
    await s33.code(ed, "public/data/results.json", 1, "03-results-json.png")
    put("types.ts", "src/types.ts")
    await s33.code(ed, "src/types.ts", 1, "04-types.png")
    put("App.tsx", "src/App.tsx")
    await s33.code(ed, "src/App.tsx", 30, "05-app.png")
    put("index.css", "src/index.css")
    await s33.code(ed, "src/index.css", 80, "06-css.png")
    await ed.palette("View: Close All Editors", 1.0)
    await s11.open_terminal(ed)
    await s11.terminal(ed, "npm run dev", 5)
    await ed.palette("View: Close Panel", 1)
    br = s33.Page()
    await br.start()
    await br.go("http://localhost:5173/monitoring/")
    await br.shot("07-dev-statusy.png")
    await br.close()
    put("check-1.yml", ".github/workflows/check.yml")
    await s33.code(ed, ".github/workflows/check.yml", 1, "08-check-yml.png")
    await ed.palette("View: Close All Editors", 1.0)
    await s33.git_push(ed, "Ночная проверка сайтов", "09-push-check.png")
    await ed.__aexit__(None, None, None)
    s33.wait_run()


def wait_check() -> None:
    """Ждёт завершения последнего запуска ночной проверки (и вызванной из неё публикации)."""
    import json
    import subprocess
    import time
    time.sleep(10)
    for _ in range(80):
        out = subprocess.run(["gh", "run", "list", "-R", "MaximBytecamp/monitoring", "--workflow", "check.yml",
                              "--limit", "1", "--json", "status,conclusion"], capture_output=True, text=True).stdout
        run = json.loads(out)[0]
        if run["status"] == "completed":
            print("  ночная проверка:", run["conclusion"])
            return
        time.sleep(5)
    raise SystemExit("запуск не завершился")


async def stage_perm() -> None:
    ed = await s33.editor()
    put("check-2.yml", ".github/workflows/check.yml")
    await s33.code(ed, ".github/workflows/check.yml", 8, "12-check-permissions.png")
    await ed.palette("View: Close All Editors", 1.0)
    await s33.git_push(ed, "Право записи для ночной проверки", "13-push-perm.png")
    await ed.__aexit__(None, None, None)
    s33.wait_run()
    gh("dispatch", "14")
    wait_check()
    gh("run", "15")
    gh("commits", "16")
    await asyncio.sleep(15)
    await site("17-sayt-staryy.png")
    gh("list", "18")


async def stage_publish() -> None:
    ed = await s33.editor()
    put("deploy.yml", ".github/workflows/deploy.yml")
    await s33.code(ed, ".github/workflows/deploy.yml", 7, "19-deploy-call.png")
    put("check.yml", ".github/workflows/check.yml")
    await s33.code(ed, ".github/workflows/check.yml", 28, "20-check-publish.png")
    await ed.palette("View: Close All Editors", 1.0)
    await git_pull_push(ed, "Публикация после ночной проверки", "21-pull-push.png")
    await ed.__aexit__(None, None, None)
    s33.wait_run()
    gh("dispatch", "22")
    wait_check()
    gh("run", "23")
    await asyncio.sleep(20)
    await site("24-sayt-novyy.png")
    gh("list", "25")


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    stages = {"local": stage_local, "perm": stage_perm, "publish": stage_publish}
    if len(sys.argv) != 2 or sys.argv[1] not in stages:
        raise SystemExit("стадии: " + ", ".join(stages))
    asyncio.run(stages[sys.argv[1]]())
