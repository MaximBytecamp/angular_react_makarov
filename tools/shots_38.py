"""Кадры автоматизации А3 «Ночная проверка сайтов и оповещение» (Telegram из GitHub Actions).

Продолжает проект /private/tmp/student/monitoring и репозиторий MaximBytecamp/monitoring после главы 3.4.
Секреты TELEGRAM_TOKEN и TELEGRAM_CHAT_ID задаются командой gh secret set до съёмки; кадры GitHub — gh38.mjs.

    python3 tools/shots_38.py all
    python3 tools/shots_38.py remove
"""
import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import shots_33 as s33  # noqa: E402
import shots_34 as s34  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/38-opoveshchenie/img/raw"
s33.IMG = IMG
CODE = Path(__file__).parent / "code38"
PROJECT = s33.PROJECT


def put(name: str, dest: str) -> None:
    shutil.copy(CODE / name, PROJECT / dest)


def gh(stage: str, *args: str) -> None:
    subprocess.run([f"{s33.cdp.NODE_BIN}/node", str(Path(__file__).parent / "gh38.mjs"), stage, *args], check=True)


async def all_frames() -> None:
    ed = await s33.editor()
    put("check.mjs", "scripts/check.mjs")
    await s33.code(ed, "scripts/check.mjs", 6, "01-notify.png")
    await s33.code(ed, "scripts/check.mjs", 50, "01a-changes.png")
    put("check.yml", ".github/workflows/check.yml")
    await s33.code(ed, ".github/workflows/check.yml", 25, "02-check-env.png")
    put("sites.json", "public/data/sites.json")
    await s33.code(ed, "public/data/sites.json", 8, "03-sites-test.png")
    await ed.palette("View: Close All Editors", 1.0)
    await s34.git_pull_push(ed, "Оповещение в Telegram", "06-pull-push.png")
    await ed.__aexit__(None, None, None)
    s33.wait_run()
    gh("dispatch", "07")
    s34.wait_check()
    gh("log", "08")
    gh("dispatch", "09")
    s34.wait_check()
    gh("log", "10")


async def remove_test() -> None:
    """Тестовый сайт убирается из списка: git pull забирает результаты двух проверок."""
    ed = await s33.editor()
    shutil.copy(Path(__file__).parent / "code33/sites.json", PROJECT / "public/data/sites.json")
    await s33.code(ed, "public/data/sites.json", 7, "11-sites-bez-testa.png")
    await ed.palette("View: Close All Editors", 1.0)
    await s34.git_pull_push(ed, "Тестовый сайт убран из списка", "12-pull-push.png")
    await ed.__aexit__(None, None, None)


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["all"]:
        asyncio.run(all_frames())
    elif sys.argv[1:] == ["remove"]:
        asyncio.run(remove_test())
    else:
        raise SystemExit("стадии: all")
