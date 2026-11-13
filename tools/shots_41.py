"""Кадры главы 4.1: тесты компонентов приложения «Мониторинг сайтов группы».

Продолжает проект /private/tmp/student/monitoring после проекта П3 (клон MaximBytecamp/monitoring).
Помощники (окно VS Code, кадр кода, кадр терминала, браузер с адресной строкой) — из shots_33.py.
Этапы те же, что проверяет tools/verify_41.sh.

    python3 tools/shots_41.py all
"""
import asyncio
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import shots_11 as s11  # noqa: E402
import shots_33 as s33  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/41-testy-komponentov/img/raw"
s33.IMG = IMG
# Порт 9361 бывает занят Chrome соседней съёмки (профиль gh41).
s33.cdp.PORT = 9362
CODE = Path(__file__).parent / "code41"
P3 = Path(__file__).parent / "proekt3-monitoring/src"
PROJECT = s33.PROJECT
INSTALL = ("npm install -D vitest@5.1.0 jsdom@31.0.0 @testing-library/react@16.3.3 @testing-library/dom@10.4.2"
           " @testing-library/user-event@14.6.10 @testing-library/jest-dom@7.0.1")


def put(name: str, dest: str) -> None:
    (PROJECT / dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(CODE / name, PROJECT / dest)


def reset() -> None:
    """Проект в состоянии после П3: без пакетов тестов и без файлов тестов."""
    for f in list((PROJECT / "src").rglob("*.test.ts*")) + [PROJECT / "src/plural.ts", PROJECT / "src/setupTests.ts"]:
        f.unlink(missing_ok=True)
    shutil.copy(P3 / "pages/SitesPage.tsx", PROJECT / "src/pages/SitesPage.tsx")
    shutil.copy(P3 / "status.ts", PROJECT / "src/status.ts")
    import subprocess
    subprocess.run(["git", "checkout", "--", "package.json", "package-lock.json", "vite.config.ts",
                    ".github/workflows/deploy.yml", "public/data/results.json"], cwd=PROJECT, check=True)
    subprocess.run([f"{s33.cdp.NODE_BIN}/npm", "ci", "--cache", "/private/tmp/student/npm-cache"], cwd=PROJECT,
                   check=True, capture_output=True, env={"PATH": f"{s33.cdp.NODE_BIN}:/usr/bin:/bin"})


async def watch_shot(ed, name: str, wait: float = 3.0) -> None:
    """Vitest в режиме наблюдения сам перезапускает тесты после сохранения файла."""
    await asyncio.sleep(wait)
    await s33.term(ed, name)


async def stage_all() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    reset()
    ed = await s33.editor()

    # §2. Установка и первый тест.
    await s11.open_terminal(ed)
    await s11.terminal(ed, INSTALL, 25)
    await s33.term(ed, "01-npm-install.png")
    await ed.palette("Terminal: Clear", 0.8)
    await s11.terminal(ed, "npm pkg set scripts.test=vitest", 2)
    await ed.palette("View: Close Panel", 1)
    await s33.code(ed, "package.json", 1, "02-package-json.png")
    put("status.test.ts", "src/status.test.ts")
    await s33.code(ed, "src/status.test.ts", 1, "03-status-test.png")
    await ed.palette("View: Close All Editors", 1.0)
    await ed.palette("View: Toggle Panel Visibility", 1.0)
    await ed.palette("Terminal: Clear", 0.8)
    await s11.terminal(ed, "npm test", 6)
    await s33.term(ed, "04-npm-test.png")
    put("status-slomano.ts", "src/status.ts")
    await watch_shot(ed, "05-test-upal.png")
    shutil.copy(P3 / "status.ts", PROJECT / "src/status.ts")
    await watch_shot(ed, "06-snova-zeleno.png")
    await ed.palette("View: Close Panel", 1)

    # §3. Тест страницы: jsdom, Testing Library.
    put("vite.config.ts", "vite.config.ts")
    await s33.code(ed, "vite.config.ts", 1, "07-vite-config.png")
    put("setupTests.ts", "src/setupTests.ts")
    await s33.code(ed, "src/setupTests.ts", 1, "08-setup-tests.png")
    put("SitesPage-1.test.tsx", "src/pages/SitesPage.test.tsx")
    await s33.code(ed, "src/pages/SitesPage.test.tsx", 1, "09-sitespage-test.png")
    await ed.palette("View: Close All Editors", 1.0)
    await ed.palette("View: Toggle Panel Visibility", 1.0)
    # vite.config.ts изменился — Vitest перезапускается целиком.
    await watch_shot(ed, "10-tri-testa.png", 6)

    # §4. Тесты по требованиям находят две ошибки.
    put("SitesPage.test.tsx", "src/pages/SitesPage.test.tsx")
    await watch_shot(ed, "11-dva-krasnyh.png", 4)
    await ed.palette("View: Close Panel", 1)
    (PROJECT / "public/data/results.json").write_text(json.dumps({"history": []}) + "\n")
    await s11.open_terminal(ed)
    await s11.terminal(ed, "npm run dev", 5)
    await ed.palette("View: Close Panel", 1)
    br = s33.Page()
    await br.start()
    await br.go("http://localhost:5173/monitoring/")
    await br.shot("12-bez-proverok.png")
    await br.close()
    await ed.palette("Terminal: Kill the Active Terminal Instance", 1.0)
    await ed.palette("View: Close Panel", 1)
    import subprocess
    subprocess.run(["git", "checkout", "--", "public/data/results.json"], cwd=PROJECT, check=True)
    put("plural.ts", "src/plural.ts")
    await s33.code(ed, "src/plural.ts", 1, "13-plural.png")
    put("SitesPage.tsx", "src/pages/SitesPage.tsx")
    await s33.code(ed, "src/pages/SitesPage.tsx", 1, "14-sitespage.png")
    await ed.palette("View: Close All Editors", 1.0)
    await ed.palette("View: Toggle Panel Visibility", 1.0)
    await watch_shot(ed, "15-ispravleno.png", 4)

    # §5. Щелчок по карточке и ошибка загрузки.
    await ed.palette("View: Close Panel", 1)
    put("App.test.tsx", "src/App.test.tsx")
    await s33.code(ed, "src/App.test.tsx", 1, "16-app-test.png")
    put("MonitoringProvider.test.tsx", "src/MonitoringProvider.test.tsx")
    await s33.code(ed, "src/MonitoringProvider.test.tsx", 1, "17-provider-test.png")
    put("plural.test.ts", "src/plural.test.ts")
    await s33.code(ed, "src/plural.test.ts", 1, "18-plural-test.png")
    await ed.palette("View: Close All Editors", 1.0)
    # Новый запуск: первый прогон в режиме наблюдения показывает все файлы тестов.
    await ed.palette("Terminal: Kill All Terminals", 1.5)
    await s11.open_terminal(ed)
    await s11.terminal(ed, "npm test", 3)
    await watch_shot(ed, "19-vse-testy.png", 4)

    # §6. Тест, списанный с текущего поведения, ошибку не замечает.
    shutil.copy(P3 / "pages/SitesPage.tsx", PROJECT / "src/pages/SitesPage.tsx")
    put("SitesPage-kopiya.test.tsx", "src/pages/SitesPage.test.tsx")
    await watch_shot(ed, "20-kopiya-zelenaya.png", 4)
    put("SitesPage.tsx", "src/pages/SitesPage.tsx")
    put("SitesPage.test.tsx", "src/pages/SitesPage.test.tsx")
    await asyncio.sleep(3)
    await ed.type("q", 1.5)
    await ed.palette("View: Close Panel", 1)

    # §7. Тесты в конвейере публикации.
    put("deploy.yml", ".github/workflows/deploy.yml")
    await s33.code(ed, ".github/workflows/deploy.yml", 30, "21-deploy-yml.png")
    await ed.palette("View: Close All Editors", 1.0)
    await s11.open_terminal(ed)
    await ed.palette("Terminal: Clear", 0.8)
    await s11.terminal(ed, "CI=true npm test", 6)
    await s33.term(ed, "22-ci-true.png")
    await ed.__aexit__(None, None, None)


if __name__ == "__main__":
    asyncio.run({"all": stage_all}[sys.argv[1]]())
