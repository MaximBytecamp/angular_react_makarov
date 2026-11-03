"""Кадры страницы проекта модуля 3 «Мониторинг сайтов группы»: пример решения на GitHub Pages.

Пример — tools/proekt3-monitoring (только локально), опубликован в демо-репозитории MaximBytecamp/monitoring
на время съёмки. Над кадрами — адресная строка (addrbar.py).

    python3 tools/shots_39.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import shots_33 as s33  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "temy/39-proekt-monitoring/img/raw"
s33.IMG = IMG
SITE = "https://maximbytecamp.github.io/monitoring/"


async def main() -> None:
    br = s33.Page()
    await br.start()
    await br.go(SITE)
    await br.shot("01-spisok.png")
    await br.page.locator("a.site", has_text="Старый проект").click()
    await br.page.wait_for_timeout(1500)
    await br.shot("02-sayt.png")
    await br.page.get_by_role("link", name="О проверке").click()
    await br.page.wait_for_timeout(1000)
    await br.shot("03-o-proverke.png")
    # Прямая ссылка в новой вкладке: файла по этому пути нет, Pages отдаёт 404.html с приложением.
    page = await br.ctx.new_page()
    response = await page.goto(SITE + "site/git")
    print("  код ответа прямой ссылки:", response.status)
    await page.wait_for_timeout(2500)
    br.page = page
    await br.shot("04-pryamaya-ssylka.png")
    await br.close()


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    asyncio.run(main())
