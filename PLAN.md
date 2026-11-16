# Справочник по Angular и React — карта книги

Отдельный продукт по образцу справочника по MongoDB: тот же каркас (корешок,
лист, паспорт главы, «В этой главе», «Проверьте себя», итог, источники),
своя палитра (React `#0A7EA4`, Angular `#C2185B`, угольный `#161A2E`) и свои блоки.

## Принцип порядка

Решение автора 14.10.2026: основной фреймворк — React, Angular — одна обзорная пара в модуле 4.
Цель — понять устройство веб-приложения и собрать небольшое приложение с автоматизацией,
не стать фронтенд-разработчиком. Каждый модуль = теория React для проекта → проект на React
(3–6 экранов) → автоматизация (бот, модель, расписание). Только бесплатные инструменты:
React+Vite, PocketBase, n8n в Docker, Ollama / GigaChat, Telegram Bot API, GitHub Pages/Actions.

## Модули (6 недель = 30 пар; 4 недели = 20: модуль 4 самостоятельно, модули 3 и 5 по 3 пары)

| Модуль | Тема | Пар | Проект | Автоматизация |
|---|---|---|---|---|
| 0 | Фронтенд в эпоху ИИ | 2 | задание: вакансии + проверка кода генератора | — |
| 1 | React: первый проект и первый бот | 6 | доска заявок | заявка → n8n → Telegram |
| 2 | Данные с сервера и ИИ-диспетчер | 6 | доска заявок с PocketBase | модель сортирует, кнопки «Взять» в Telegram |
| 3 | Несколько экранов, публикация, расписание | 5 | мониторинг сайтов группы | GitHub Actions ночью, Playwright, Lighthouse |
| 4 | Работа с ИИ-агентом и обзор Angular | 6 | дайджест новостей (Р2) | RSS → модель → Telegram |
| 5 | Свой проект и защита | 5 | каталог: сторож страницы, чек → бюджет, голос → задачи, ассистент по конспектам, карта | — |

## Модуль 0

- 0.1 `temy/01-frontend-i-freymvorki` — фронтенд и бэкенд, лента лет, состояние
  и интерфейс (живая витрина), компоненты, что берёт на себя фреймворк.
- 0.2 `temy/02-react-i-angular` — кто разрабатывает, версии, опрос Stack Overflow 2025,
  поиск по городам на двух фреймворках, различия, фреймворки и инструменты ИИ.
- 0.3 `temy/03-ii-vo-frontende` — четыре уровня инструментов, как модель пишет код,
  измерения (GitHub, METR, Airbnb, Google), доверие разработчиков, карта задач.
- Отдельный разбор `razbor-zamenil-li-ii/` (бывшая глава 0.4) — «Заменил ли ИИ фронтенд-разработчика»:
  рынок труда, 3 удачи, 5 неудач, история Builder.ai, ответ. По решению автора 14.10.2026 вынесен
  из списка глав в отдельную карточку на обложке; ссылка на него есть в конце §5 главы 0.3.
- 0.5 `temy/05-kak-ustroena-disciplina` — цели, порядок модулей, режимы Р0/Р1/Р2,
  цикл работы с агентом, список проверки, задание к модулю 0.

## Правила текста

Как в справочнике по MongoDB: `shared/TEXT_REVIEW.md`. Каждое число в модуле 0
взято из источника, ссылка стоит в главе. Материалы с коммерческим интересом автора
помечаются `.vendor`. Числа и даты в пиксельном шрифте не набирать — только моноширинным.

## Модуль 1

- 1.1–1.4 — проект `zayavki`: Vite, JSX и компоненты, props, состояние и события.
- 1.5 `temy/15-spiski-i-usloviya` — массив заявок в `src/requests.ts`, `map` и `key`, опыт с изменением
  массива на месте, новый массив через `map` и `{ ...r }`, `filter`, условный вывод (`&&`, тернарный),
  удаление, фильтр по статусу, опыт с `key={index}`.
- 1.7 `temy/17-sohranenie-i-otpravka` — localStorage (`storage.ts`, `update`), `fetch` POST на вебхук n8n (`notify.ts`),
  доска работает при выключенном n8n.
- Проект П1 `temy/19-proekt-doska-zayavok` — варианты «Общежитие», «Студсовет», свой; требования, режим Р1, журнал `ai-log.md`, защита.
  Пример варианта — `tools/proekt-obshchezhitie`.
- Автоматизация А1 `temy/18-avtomatizaciya` — Docker + `compose.yaml` (n8n 2.45.4), бот @BotFather, getUpdates, шаблон процесса
  `tools/n8n/zayavka-telegram.json` вставляется Ctrl+V, Publish. Кадры `tools/shots_n8n.py` (токен из файла, номер чата размыт).
  Кадры @BotFather (токен размыт) и сообщения бота — снимки автора, a00 и a17.
- 1.6 `temy/16-formy` — категория в данных (`Category`, `NewRequest`), управляемые поля (`value` + `onChange`,
  опыт без `onChange`), отправка (`onSubmit`, `preventDefault`, `[created, ...requests]`, `Date.now()`),
  проверка полей с `trim()` и сообщением об ошибке. Тип события — `SubmitEvent` (`FormEvent` в @types/react помечен устаревшим).

## Архивы проекта и разбор кода

- В каждой главе модуля 1 блок `.starter` с архивом начала главы и `.starter--finish` с архивом конца.
  Архивы собирает `tools/pack.py` из `tools/codeNN` (без `node_modules`); `--check` распаковывает каждый
  и выполняет `npm ci`, `tsc -b`, `oxlint`, `vite build`. Новая глава — новая строка в `ARCHIVES`.
- Пошаговый разбор `.trace` (book.js): код слева (`<!--CODE … | | bare lines=A-B-->`), шаги справа
  с `data-lines` по номерам строк файла; в шагах — ячейки памяти `.var`, массив `.arr`, мини-карточки `.mini`.
- Код с номерными метками: `pins=строка:номер` в маркере CODE и список `.anno` под блоком.

## Модуль 2

Порядок (решение автора 29.10.2026): 2.1 Эффекты → 2.2 PocketBase: коллекции и правила → 2.3 Загрузка: загрузка и ошибка →
2.4 Собственный хук → 2.5 Обновление по событиям. Прототип всего модуля — `tools/proto2` (PocketBase 0.40.6 из своего
Dockerfile, n8n 2.45.4, Ollama + qwen2.5:3b из GGUF с Hugging Face; кнопки Telegram опросом getUpdates).

- 2.1 `temy/21-effekty` — заголовок вкладки, исчезающее сообщение (таймер + очистка), Esc через подписку на окно;
  опыты с журналом в консоли (StrictMode), пропущенная зависимость (exhaustive-deps), visible через эффект (set-state-in-effect).
- 2.2 `temy/22-pocketbase` — PocketBase в Docker (свой Dockerfile, `code22/compose.yaml` = n8n + pocketbase), суперпользователь
  командой `superuser upsert`, коллекция requests через панель, правила: list/view пусто, create `status = "Новая"`,
  update без title/room/details (категорию можно править — ошибки модели), delete `status = "Готово"`; проверка из консоли.
  Съёмка `tools/shots_22.py` (перед кадрами VS Code открыть App.tsx — иначе видны ошибки прошлого сеанса).
- 2.3 `temy/23-zagruzka` — `api.ts` (`callApi`: сеть → «Сервер заявок не отвечает», `!response.ok` → «код N»; `fetchRequests`
  с `?sort=-created`, затем `createRequest`/`updateStatus`/`deleteRequest`), `storage.ts` удалён, `id: string`; эффект загрузки
  с флажком `ignore` (два запроса в Network из-за StrictMode), опыты: заявка пропадает после F5, PocketBase остановлен
  (вечная загрузка → `try/catch`, `error`, кнопка «Повторить» через зависимость `attempt`), действие без сервера → `notice`;
  функция обновления `setRequests((list) => …)`. Код `tools/code23`, съёмка `shots_23.py` (база перед съёмкой приводится
  к пяти «Новая»; задержка ответа — `page.route`), обрезка `crop_23.py`. После главы в базе 6 заявок.
- 2.4 `temy/24-sobstvennyy-huk` — хук `useRequests` в два шага (загрузка → действия add/next/remove, `setRequests` наружу
  не выходит; try/catch остаётся в обработчиках App), опыт «Header сам вызывает хук» (4 запроса, счётчик расходится),
  опыт «return перед хуком» (oxlint rules-of-hooks, «Rendered fewer hooks than expected»), разбор порядка ячеек хуков.
  Код `tools/code24`, съёмка `shots_24.py`, обрезка `crop_24.py`. После главы в базе 7 заявок («Нет звука в колонках» в работе).
- 2.5 `temy/25-obnovlenie-po-sobytiyam` — опыт с двумя окнами (без F5 заявки не видно), опрос и SSE, `npm install pocketbase@0.28.1`,
  `realtime.ts` (`subscribe('*')`, отписка через `pending.then`), эффект подписки в хуке; опыт с повтором своей заявки
  (ответ POST + событие create, предупреждение о ключах) → `upsertRequest` в `requests.ts`; правка категории в панели доходит до доски;
  поток во вкладке Network → realtime → EventStream. Код `tools/code25` (+ package.json/lock с библиотекой: pack.py принимает ключи
  `/package.json`), съёмка `shots_25.py` (пары окон рядом; DevTools открывать до второго окна), обрезка `crop_25.py`.

- Автоматизация А2 `temy/28-ii-dispetcher` — Ollama 0.40.12 в `code28/compose.yaml` (+ `TELEGRAM_TOKEN` из `.env`,
  `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`), модель qwen2.5:3b (запасной путь — GGUF с Hugging Face + `ollama create`),
  шаблоны `tools/n8n2/ii-dispetcher.json` (вебхук → модель с JSON-схемой → PATCH category → Telegram с кнопкой take:id)
  и `knopka-vzyat.json` (раз в 10 с getUpdates, offset = последний + 1, PATCH status, answerQuery, editMessageText,
  On Error → Continue от двойного нажатия). Замер модели: категория 4/6, срочность 6/6, ~2 с на заявку.
  Съёмка `shots_28.py` (all / part2), снимки Telegram — от автора (b18–b20, имя размыто).
- Проект П2 `temy/29-proekt-doska-s-bazoy` — вариант П1 переезжает на PocketBase: своя коллекция с правилами 2.2, хук,
  события, ИИ-диспетчер со своими категориями (процессы А2 правятся на месте: getUpdates отдаёт нажатие одному процессу).
  Пример «Общежитие»: `tools/proekt2-obshchezhitie` (отличия: Category, имя коллекции в api.ts/realtime.ts), коллекция
  obshchezhitie в PocketBase студента, съёмка `shots_p2.py`. Модуль 2 закончен.

## Модуль 3

Решения автора 30.10.2026: 3.1 Маршрутизация и 3.2 Контекст — на доске заявок; 3.3 GitHub Pages, 3.4 GitHub Actions, проект и
автоматизация — на приложении «Мониторинг сайтов группы» (доске нужен PocketBase на localhost). Сначала прототип.

Прототип — `tools/proto3` (рабочая копия /private/tmp/student/proto3/monitoring), репозиторий github.com/MaximBytecamp/monitoring-demo,
сайт maximbytecamp.github.io/monitoring-demo/. react-router 8.5.1 (BrowserRouter с basename = BASE_URL, Routes/Route, вложенный
маршрут с Outlet, NavLink, useParams), контекст в `monitoring.ts` + `MonitoringProvider.tsx` (без нарушения only-export-components),
данные `public/data/sites.json` и `results.json` (30 последних проверок), Vite `base: '/monitoring-demo/'`.
`scripts/check.mjs`: Playwright 1.64.1 (только headless shell) открывает сайты, Lighthouse 13.6.0 через порт отладки 9333 даёт
скорость и доступность, при падении — сообщение в Telegram (секреты TELEGRAM_TOKEN, TELEGRAM_CHAT_ID).
`deploy.yml` (push, workflow_dispatch, workflow_call; checkout ref: main; cp index.html 404.html) и `check.yml` (cron 0 21 * * * =
00:00 МСК; коммит результатов от github-actions[bot]; затем `uses: ./.github/workflows/deploy.yml` — коммит GITHUB_TOKEN новые
запуски не порождает). Замеры: проверка 6 сайтов локально 42 с, в Actions весь запуск 1 мин 41 с; прямая ссылка на Pages отдаёт код
404 с приложением внутри (404.html) — для 3.3 сравнить с HashRouter. Версии действий: checkout@v7, setup-node@v7,
upload-pages-artifact@v5, deploy-pages@v5.

- 3.1 `temy/31-marshrutizaciya` — опыт «/stats до роутера = та же доска», `npm install react-router@8.5.1`, `BrowserRouter` в `main.tsx`,
  страницы в `src/pages` (BoardPage — фильтр, Esc, форма и список из App; StatsPage — две таблицы; NotFoundPage с `useLocation`;
  RequestPage с `useParams`, `useNavigate`, `find`), маршруты `/`, `/stats`, `/requests/:id`, `*`; `notice` под шапкой для всех страниц;
  опыт `<a href>` (31 запрос в Network) против `NavLink` (запросов нет; `end` для `/` в v8 не нужен); сброс фильтра при уходе со страницы;
  §5 — 14 props через App как подводка к 3.2. Код `tools/code31` (стили — `index-add.css` в конец index.css), проверка всех
  промежуточных состояний `tools/verify_31.sh`, съёмка `shots_31.py` (база — `code31/db-start.json`, адресная строка над кадрами
  браузера дорисовывается `addrbar.py` из `page.url`), обрезка `crop_31.py`.
- 3.2 `temy/32-kontekst` — проброс props (14 через App), `board.ts` (тип Board, `createContext<Board | null>(null)`, `useBoard`
  с ошибкой «useBoard вызван вне BoardProvider»), `BoardProvider.tsx` (код App без изменений, `children: ReactNode`,
  `<BoardContext value={board}>` — запись React 19), опыт без провайдера в main.tsx, страницы и шапка читают `useBoard`,
  App — 26 строк; опыт «взять в работу на странице заявки → счётчик шапки 6→5, статистика совпадает» против опыта 2.4;
  что класть в контекст. Код `tools/code32`, проверка `verify_32.sh`, съёмка `shots_32.py` (база `code32/db-start.json`), `crop_32.py`.
- 3.3 `temy/33-github-pages` — решение автора 02.11.2026: приложение мониторинга у студента — отдельный публичный репозиторий
  `monitoring` рядом с react-kurs; в 3.3 только список сайтов из `public/data/sites.json` (fetch + ignore). Сборка в dist, file://
  не работает (CORS), `npm run preview`; репозиторий через github.com/new и команды из терминала; Settings → Pages → Source:
  GitHub Actions; `.github/workflows/deploy.yml` (одно задание: checkout@v7, setup-node@v7 24 + cache npm, npm ci, build,
  upload-pages-artifact@v5, deploy-pages@v5). Опыт из трёх публикаций: без base — пустая страница (404 /assets), base
  '/monitoring/' — 404 на /data/sites.json, `import.meta.env.BASE_URL` — работает. §6 — 404.html и basename для маршрутов
  (Pages на /monitoring/nope отдаёт 404 «File not found»). Код `tools/code33`, съёмка `shots_33.py` (стадии local/push/deploy/
  base/url), кадры GitHub — `gh33.mjs` (Chrome ~/repo-shots-chrome, порт 9381, headless), `crop_33.py`; hl.py понимает YAML.
  Демо-репозиторий github.com/MaximBytecamp/monitoring после съёмки закрыт (private), для 3.4 открыть снова.
- 3.4 `temy/34-github-actions` — `scripts/check.mjs` (fetch + AbortSignal.timeout(15000), история 30 проверок в
  `public/data/results.json`), статусы в App (`loadJson`, `statusText`, `?.`), `check.yml` в три шага на настоящих запусках:
  без permissions — 403 «denied to github-actions[bot]»; `contents: write` — коммит бота есть, сайт старый (коммиты GITHUB_TOKEN
  не запускают push-конвейеры); задание `publish` с `uses: ./.github/workflows/deploy.yml`, в deploy.yml `workflow_call` и
  `checkout ref: main`, `git pull` перед отправкой — сайт с временем запуска на GitHub (весь путь 1 мин 56 с). Cron в UTC
  (0 21 * * * = 00:00 МСК), 60 дней без активности. Код `tools/code34`, съёмка `shots_34.py` (local/perm/publish, помощники
  из shots_33), кадры GitHub `gh34.mjs` (рамки в своём popover поверх окон Primer), `crop_34.py`.
  Telegram, Playwright/Lighthouse, страницы сайта и история — автоматизация А3 и проект модуля 3.
- Автоматизация А3 `temy/38-opoveshchenie` — секреты TELEGRAM_TOKEN/TELEGRAM_CHAT_ID (Settings → Secrets and variables → Actions,
  на кадре значение размыто, сами секреты заданы `gh secret set`), `env` у шага проверки, `notify()` в check.mjs (process.env,
  sendMessage), сообщение только об изменениях (сравнение с `history[1]`). Два запуска: тестовый сайт monitoring-test → Telegram: 200,
  повтор → «Изменений нет»; в журнале секреты `***`; ночной запуск №4 по расписанию начался в 05:46 МСК вместо 00:00.
  Код `tools/code38`, съёмка `shots_38.py` (all/remove), `gh38.mjs` (журнал шага по ссылке `#step:N:1`), `crop_38.py`.
  Кадр сообщения бота в Telegram (img/09-telegram.png) — снимок автора, второе из двух сообщений (09:05, запуск №7).
- Проект П3 `temy/39-proekt-monitoring` — один вариант на всех, список — сайты своей группы (мониторы однокурсников); маршруты
  /, /site/:id, /about, *; контекст MonitoringProvider/useMonitoring; история на странице сайта; basename и 404.html; ночная
  проверка и оповещение без изменений. Пример — `tools/proekt3-monitoring` (только локально), кадры `shots_39.py` с Pages
  (прямая ссылка /site/git — код 404 и приложение из 404.html), `crop_39.py`. Сдача: код в репозитории monitoring,
  в react-kurs — `projects/p3-monitoring` с README (ссылки) и ai-log.md (строка в шаблоне react-kurs-template). Модуль 3 закончен.

## Модуль 4

Решения автора 13.11.2026: 4.1 Тесты компонентов и 4.2 Доступность — на «Мониторинге сайтов группы» (продолжение П3, код примера
`tools/proekt3-monitoring`; тесты запускаются шагом в deploy.yml). Агент для 4.3 и проекта — локальный: расширение VS Code
с моделью в Ollama. Хранилище дайджеста — Firebase (Firestore), запасной путь — PocketBase.

- 4.1 `temy/41-testy` (план, прототип проверен 13.11.2026 в scratchpad `proto4/monitoring`): `npm install -D vitest@5.1.0 jsdom@31.0.0
  @testing-library/react@16.3.3 @testing-library/dom@10.4.2 @testing-library/user-event@14.6.10 @testing-library/jest-dom@7.0.1`,
  `test` в vite.config (из `vitest/config`: environment jsdom, setupFiles), `setupTests.ts` (jest-dom + cleanup — без globals
  автоочистки нет), скрипт `"test": "vitest"` (дома — режим наблюдения, при CI=true — один прогон). Порядок: тест функции
  `statusText` → тест страницы SitesPage (MemoryRouter + MonitoringContext с придуманными данными, getByText/getByRole) →
  тесты по требованиям находят две настоящие ошибки П3: «Все 3 сайтов открываются» и «Не открываются: 3 из 3» без проверок →
  исправление (`plural.ts`/`sitesWord`, строка `summary`) → щелчок userEvent по карточке (App.test) → подмена fetch
  `vi.stubGlobal` (ошибка «Файл sites.json не загрузился: код 404.») → тест, переписанный с текущего поведения, ошибку
  пропускает → шаг «Запустить тесты» в deploy.yml. Код `tools/code41` (SitesPage-p3.tsx — исходный код П3). 19 тестов, 1 с.
  Готова 13.11.2026 (b94c3ad), `temy/41-testy-komponentov`, съёмка `shots_41.py` (порт 9362), обрезка `crop_41.py`.
- 4.2 `temy/42-dostupnost` (прототип 13–15.11.2026, код `tools/code42`, этапы `verify_42.sh` — 8 этапов сходятся).
  Lighthouse 13.6.0 (DevTools, только Accessibility): «Сайты» 94, страница сайта 91, «О проверке» 100 — всё color-contrast
  (зелёный статус #2e9d5b 3,44:1, ссылки #2f6fde 4,36:1 на #f5f6f9) → #1e7a46 (5,35) и #2563d0 (5,15) → 100 и 100.
  Опыт: карточка `div onClick` + useNavigate (как пишет агент) — Lighthouse всё равно 100, Tab карточки пропускает,
  2 теста 4.1 по роли link падают, oxlint с плагином jsx-a11y: click-events-have-key-events, no-static-element-interactions.
  Дерево доступности (DevTools → Accessibility): имя ссылки-карточки начиналось со статуса → тест `name: /^Справочник/`
  красный → h2 первым. Заголовки вкладок: React 19 `<title>` в каждой странице (ставится в head перед статическим из
  index.html, document.title берёт его) + проверка document.title в App.test. role="status" (загрузка), role="alert"
  (ошибка), caption в таблице истории; тесты getByRole('status')/findByRole('alert'). Правило jsx-a11y/prefer-tag-over-role
  (советует <output>) выключено в .oxlintrc.json с объяснением. Шаг «Проверить код линтером» (`npm run lint -- --deny-warnings`)
  в deploy.yml перед тестами. Итог 20 тестов. Факты: WebAIM Million 2026 (95,9 %, контраст 83,9 %), ВОЗ 2,2 млрд (10.02.2026),
  ГОСТ Р 52872-2019 на основе WCAG 2.1, WCAG 1.4.3 — 4,5:1 и 3:1.
- 4.3 `temy/43-zadacha-agentu` (прототип 16.11.2026, не закончен). Задание агенту — `tools/code43/zadanie.md` (поиск и флажок
  «Только неработающие» на странице «Сайты»), эталон `SitesPage-etalon.tsx`, приёмка `priemka.test.tsx` (7 тестов, с эталоном 27/27).
  Агент: Continue 2.0.0 (Continue.continue) в отдельном профиле VS Code `/private/tmp/vsc-agent` (порт 9363), настройки
  `CONTINUE_GLOBAL_DIR=/private/tmp/vsc-agent/continue` (config.yaml: provider ollama, capabilities tool_use, contextLength 16384).
  Модель: qwen3:4b из GGUF Hugging Face (Qwen/Qwen3-4B-GGUF Q4_K_M; реестр Ollama через VPN не качает — R2 резолвится в 240.0.0.x),
  `ollama create`; Ollama 0.40.12 в Docker (контейнер ollama43, том proto2_ollama_data). CPU: чтение 82 ток/с, генерация 10 ток/с.
  Docker VM 4 ГБ: с KV q8_0 и 16k контейнер OOMKilled; с q4_0 модель занимает 3,1 из 3,8 ГБ. Прогон 2: агент прочитал файл и выдал
  код в чат (не инструментом правки), Apply → «Could not resolve filepath to apply changes»; код: useEffect+setSelectedSites (нарушение
  правила), английские подписи, aria-label поверх label, `/sites/` вместо `/site/`, несуществующий site.status, сводка пропала.
  Управление панелью Continue — сырой CDP к цели iframe (scratchpad wv.py), data-testid: mode-select-button, submit-input-button.
  16.11.2026, продолжение. Ollama 0.40.16 нативно (`/private/tmp/ollama-mac`, OLLAMA_MODELS=./models, Metal: 33 ток/с). Официальные
  модели качаются через `curl` по манифесту registry.ollama.ai (сама Ollama отказывается: R2 → 240.0.0.x) — скрипт `/private/tmp/gguf/fetch.py`.
  qwen3:4b (с рассуждением) не годится: рассуждает до лимита 4096 и не вызывает инструмент; взят qwen3:4b-instruct (тот же 2,5 ГБ).
  Ловушка Continue 2.0: провайдер `ollama` шлёт tools только если последнее сообщение от user (после результата инструмента — без
  инструментов, модель пишет код в чат). Обход: `provider: openai`, `apiBase: http://localhost:11434/v1`, `apiKey: ollama`.
  AGENTS.md в корне проекта Continue вставляет в системную подсказку («1 rule · Always applied»).
  Прогоны: полное задание (r7–r9) — 0 правок, приёмка 0/7, отчёт «✅ implementation looks correct». По шагам (shag1–3.md):
  шаг 1 — правка +16 строк, агент сам запустил lint и test, но: нет import useState (tsc TS2304, 13 тестов падают), useState после
  return (oxlint rules-of-hooks error), поле под карточками, лишний пробел в чужой строке; шаг 2 — код в чат, без правки; шаг 3 — 3 теста
  в SitesPage.test.tsx без import userEvent (TS2552). Итог 16 из 30 тестов падают. Итоги прогонов — scratchpad runs/{r7,r8,r9,s1,s2,s3}.
- 4.4 `temy/44-angular` (прототип 16.11.2026 в `/private/tmp/proto44/monitoring-ng`, код `tools/code44`). Angular 22.2.6 (CLI 22.2.7):
  `ng new` по умолчанию — компоненты без NgModule, без zone.js, тесты Vitest 5 + jsdom, OnPush по умолчанию; `--ai-config=open-ai-codex`
  создаёт AGENTS.md с правилами Angular (мост к 4.3). Страница «Сайты» монитора на Angular: status.ts, plural.ts, types.ts — без изменений;
  служба `@Service()` (новое в 22) с двумя `httpResource` (стабилен с 22.0) и `computed` вместо провайдера с useEffect и контекста;
  SitesPage — signal + computed, шаблон @if/@for/track, [routerLink], [class.x]; заголовки вкладок — `title` в маршрутах;
  SitePage — `input.required` + withComponentInputBinding. Тест TestBed + Vitest, служба подменена useValue: 4 теста.
  Числа: данные 72 строки React против 27; страница 74 против 75 (46 + 29 шаблон); сборка 262 КБ против 254 КБ (в React больше страниц);
  node_modules 124 МБ / 87 пакетов против 287 МБ / 200.
- Проект П4 «Дайджест новостей» (Р2). Решение автора 16.11.2026: агент на выбор студента (облачный или Continue + Ollama из 4.3),
  оценивается процесс — задания, AGENTS.md, проверки, чтение изменений, журнал ai-log.md. Хранилище — Firebase (запасной путь — PocketBase).
  16.11.2026: хранилище — Google Таблицы (решение автора вместо Firebase: бесплатно, без карты). Таблица «Дайджест новостей»
  (аккаунт автора, лист `news`: id, date, source, title, summary, tags, link) + Apps Script «Дайджест», код `tools/code45/Code.gs`:
  `/** @OnlyCurrentDoc */` (без неё Google просит доступ ко ВСЕМ таблицам аккаунта; с ней — только к этой), doGet → {news},
  doPost с ключом из свойств скрипта KEY → добавляет новые по id, повтор не дублирует. Веб-приложение: от моего имени, доступ «Все».
  Адрес — `~/digest-url.txt`, ключ — `~/digest-key.txt` (секрет, вне Git). Проверено: GET {"news":[]}; POST без ключа → {"error":"Неверный ключ"};
  POST отвечает 302 → googleusercontent, ответ забирается GET (curl без -X POST); CORS `*` на обоих шагах; fetch со страницы github.io — ok, 5,1 с
  (холодный старт). Дата 2026-11-16 вернулась как 2026-11-15T21:00:00.000Z (таблица переводит в дату по Москве) — слать ISO со временем;
  теги возвращаются строкой «a, b». Окно Chrome для съёмки: профиль `~/firebase-shots-chrome`, порт 9391, вход в Google выполнен.
  n8n (16.11.2026): стенд `tools/code45/stand/compose.yaml` — только n8n 2.45.4, переменные DIGEST_URL, DIGEST_KEY, TELEGRAM_TOKEN,
  TELEGRAM_CHAT_ID из `.env`; модель — Ollama на компьютере (из 4.3) `qwen3:4b-instruct` по http://host.docker.internal:11434
  (qwen2.5:3b в Docker: 124–196 с на новость и выдумки; qwen3:4b-instruct: 5–10 с; схема format с массивом enum вешает Ollama
  0.40.12 — теги массивом строк, лишние отсекает Code). Процесс `n8n/sbor.json`: Каждое утро 8:00 / Запустить вручную → Ленты
  (Хабр, 3DNews, iXBT) → RSS → Свежие новости (сутки, ≤5 с сайта, id = ссылка без ?utm; в Code нет объекта URL) → Модель →
  Проверка ответа (теги из списка) → Запись в таблицу (executeOnce). Прогон: 15 новостей за 67 с, {"added": 15}.
  `n8n/vecher.json`: 19:00 → GET таблицы → текст за сутки (≤4000 знаков) → sendMessage. Запуск из CLI:
  `docker exec -e N8N_RUNNERS_BROKER_PORT=5690 digest-n8n-1 n8n execute --id=…` (нужен узел ручного запуска).
  Страница-эталон `tools/proekt4-digest` (Vite 8, React 19.3; прототип `/private/tmp/proto45/digest`): VITE_DIGEST_URL в `.env.local`,
  digest.ts (fetch, теги строкой → список, сортировка по дате), read.ts (localStorage «digest-read»), App: поиск по заголовку и пересказу,
  тег (select), «Только непрочитанные», карточки со ссылкой, источником, датой, тегами и кнопкой «Отметить прочитанным» (aria-pressed),
  role=status/alert. Проверено на настоящих данных: 15 новостей, «windows» → 2, «наука» → 3, прочитано переживает перезагрузку, 13 из 15.
  Ждёт: токен бота в `~/digest-telegram.txt` для проверки вечернего процесса. Дальше — главы: автоматизация А4 и проект П4.
