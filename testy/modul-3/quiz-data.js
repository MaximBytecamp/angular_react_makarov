/* Тест «Модуль 3 · маршруты, публикация и Actions». Ключи и разбор обфусцированы в SECRET: это барьер от беглого чтения исходника, а не защита. */

const QUIZ = {
  "id": "angular-react-test-m3",
  "prefix": "AR3",
  "title": "Модуль 3 · маршруты, публикация и Actions",
  "minutes": 35,
  "salt": "angular-react-m3-2026",
  "context": "Все задания опираются на главы 3.1–3.4, ночное оповещение и проект мониторинга сайтов группы. Используются те же React Router, контекст, GitHub Pages и GitHub Actions, что в материалах.",
  "grades": [
    {
      "min": 13,
      "mark": 5,
      "label": "отлично"
    },
    {
      "min": 10,
      "mark": 4,
      "label": "хорошо"
    },
    {
      "min": 7,
      "mark": 3,
      "label": "удовлетворительно"
    },
    {
      "min": 0,
      "mark": 2,
      "label": "неудовлетворительно"
    }
  ],
  "questions": [
    {
      "id": "q01",
      "topic": "3.1 · маршрутизация",
      "type": "slots",
      "text": "Сопоставьте часть React Router с её задачей. Две карточки лишние.",
      "chips": [
        "BrowserRouter",
        "Routes",
        "Route",
        "NavLink",
        "useParams"
      ],
      "slots": [
        "Следит за адресом и его изменениями",
        "Выбирает подходящий маршрут",
        "Описывает путь и элемент страницы"
      ]
    },
    {
      "id": "q02",
      "topic": "3.1 · переходы",
      "type": "multi",
      "text": "Чем <code>NavLink</code> отличается от обычного <code>&lt;a href&gt;</code> внутри приложения? Отметьте все верные утверждения.",
      "options": [
        "NavLink меняет адрес без полной перезагрузки приложения",
        "При NavLink список в памяти не загружается с нуля",
        "Обычная ссылка перезапускает приложение",
        "NavLink всегда отправляет новый HTTP-запрос за index.html",
        "Обычная ссылка сохраняет всё состояние компонентов"
      ]
    },
    {
      "id": "q03",
      "topic": "3.1 · параметры пути",
      "type": "single",
      "text": "Маршрут задан как <code>/requests/:id</code>, открыт адрес <code>/requests/k2m9</code>. Что вернёт <code>useParams()</code>?",
      "options": [
        "Объект <code>{ id: 'k2m9' }</code>",
        "Строку <code>'/requests/k2m9'</code>",
        "Объект <code>{ requests: 'k2m9' }</code>",
        "Число заявок на странице"
      ]
    },
    {
      "id": "q04",
      "topic": "3.1 · состояние страницы",
      "type": "single",
      "text": "Фильтр хранится в состоянии BoardPage. Почему после перехода на статистику и возврата на доску он снова равен «Все»?",
      "options": [
        "BoardPage удалился, а при возврате создался с начальным состоянием",
        "BrowserRouter очищает localStorage при каждом переходе",
        "NavLink вручную вызывает setFilter('Все')",
        "Контекст запрещает хранить фильтр"
      ]
    },
    {
      "id": "q05",
      "topic": "3.2 · части контекста",
      "type": "slots",
      "text": "Сопоставьте часть решения с файлом или ролью. Две карточки лишние.",
      "chips": [
        "board.ts",
        "BoardProvider.tsx",
        "main.tsx",
        "App.tsx",
        "Header.tsx"
      ],
      "slots": [
        "BoardContext и хук useBoard",
        "Провайдер с единственным вызовом useRequests",
        "Место, где BoardProvider оборачивает App"
      ]
    },
    {
      "id": "q06",
      "topic": "3.2 · провайдер",
      "type": "single",
      "text": "Компонент вызвал <code>useBoard()</code>, но над ним нет <code>BoardProvider</code>. Что произойдёт в реализации из главы?",
      "options": [
        "Контекст даст null, а useBoard выбросит понятную ошибку",
        "React автоматически создаст BoardProvider",
        "Хук загрузит отдельный список без контекста",
        "Компонент получит пустой массив без ошибки"
      ]
    },
    {
      "id": "q07",
      "topic": "3.2 · что хранить в контексте",
      "type": "sort",
      "text": "Разложите данные по месту хранения в приложении из главы.",
      "items": [
        "Список заявок",
        "Состояние загрузки заявок",
        "Функция изменения статуса",
        "Выбранный фильтр доски"
      ],
      "buckets": [
        "Общий контекст BoardContext",
        "Локальное состояние BoardPage"
      ]
    },
    {
      "id": "q08",
      "topic": "3.2 · единый список",
      "type": "single",
      "text": "Почему после переноса <code>useRequests()</code> в BoardProvider счётчик Header и карточки обновляются согласованно?",
      "options": [
        "Хук вызывается один раз, и все потребители читают один список",
        "Контекст копирует список отдельно в каждый компонент",
        "Header больше не перерисовывается",
        "React Router синхронизирует состояния компонентов"
      ]
    },
    {
      "id": "q09",
      "topic": "3.3 · ограничения Pages",
      "type": "single",
      "text": "Почему доску заявок с адресом PocketBase <code>localhost:8090</code> нельзя в таком виде опубликовать на GitHub Pages для других людей?",
      "options": [
        "У посетителя localhost указывает на его компьютер, где PocketBase нет",
        "GitHub Pages не поддерживает JavaScript",
        "React Router запрещён на Pages",
        "PocketBase работает только внутри VS Code"
      ]
    },
    {
      "id": "q10",
      "topic": "3.3 · src и dist",
      "type": "sort",
      "text": "Разложите элементы проекта по папке, к которой они относятся после сборки.",
      "items": [
        "Исходный TypeScript и JSX",
        "Компоненты React для разработки",
        "Готовый JavaScript-бандл",
        "Собранный CSS и index.html",
        "Копия файлов из public"
      ],
      "buckets": [
        "src",
        "dist"
      ]
    },
    {
      "id": "q11",
      "topic": "3.3 · base и BASE_URL",
      "type": "slots",
      "text": "Репозиторий называется <code>site-monitor</code>. Подставьте значения и назначения. Одна карточка лишняя.",
      "chips": [
        "/site-monitor/",
        "base",
        "BASE_URL",
        "/",
        "dist"
      ],
      "slots": [
        "Значение пути для публикации в подпапке",
        "Настройка Vite, которая меняет пути при сборке",
        "Значение для путей внутри кода, например в fetch"
      ]
    },
    {
      "id": "q12",
      "topic": "3.3 · публикация",
      "type": "order",
      "text": "После <code>git push</code> GitHub Actions публикует приложение. Расставьте основные шаги по порядку.",
      "items": [
        "Скачать код репозитория",
        "Установить Node.js и пакеты",
        "Собрать папку dist",
        "Упаковать результат как артефакт Pages",
        "Развернуть артефакт на GitHub Pages"
      ]
    },
    {
      "id": "q13",
      "topic": "3.4 · расписание",
      "type": "single",
      "text": "Когда по московскому времени сработает <code>cron: '30 4 * * 1'</code> из главы?",
      "options": [
        "Каждый понедельник в 07:30",
        "Каждый день в 04:30",
        "Каждый понедельник в 04:30",
        "Каждое первое число месяца в 07:30"
      ]
    },
    {
      "id": "q14",
      "topic": "3.4 · зависимости заданий",
      "type": "multi",
      "text": "Какие утверждения о конвейере проверки и публикации верны? Отметьте все верные варианты.",
      "options": [
        "<code>workflow_dispatch</code> добавляет ручной запуск",
        "Для <code>git push</code> боту нужно право записи",
        "<code>needs: check</code> заставляет публикацию ждать успешную проверку",
        "Коммит через GITHUB_TOKEN всегда запускает все остальные workflows",
        "Без needs задания гарантированно выполняются одно за другим"
      ]
    },
    {
      "id": "q15",
      "topic": "А3 · оповещение об изменении",
      "type": "number",
      "text": "Сайт работал. Затем он не открывался три ночи подряд. Скрипт отправляет сообщение только при изменении состояния. Сколько сообщений о падении придёт за эти три ночи? Введите число.",
      "unit": "сообщение"
    }
  ]
};

const SECRET = "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";
let SECRET_CACHE = null;
async function secretData() {
  if (SECRET_CACHE) return SECRET_CACHE;
  const bytes = Uint8Array.from(atob(SECRET), c => c.charCodeAt(0));
  const plain = bytes.map((b, i) => b ^ QUIZ.salt.charCodeAt(i % QUIZ.salt.length));
  SECRET_CACHE = JSON.parse(new TextDecoder().decode(plain));
  return SECRET_CACHE;
}

async function shortHash(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('').slice(0, 16);
}

function normalized(q, a) {
  if (a == null) return null;
  switch (q.type) {
    case 'single': case 'multi': case 'line': return a.length ? [...a].sort((x, y) => x - y) : null;
    case 'order': return a.length ? a : null;
    case 'slots': case 'sort': return a.every(x => x !== null && x !== undefined) ? a : null;
    case 'number': {
      const s = String(a).replace(/\\s/g, '').replace(',', '.');
      return s !== '' && isFinite(Number(s)) ? [Number(s)] : null;
    }
  }
  return null;
}

async function isCorrect(q, a) {
  const norm = normalized(q, a);
  if (!norm) return false;
  return JSON.stringify(norm) === JSON.stringify((await secretData())[q.id].key);
}

function encodeAnswer(q, a) {
  if (a == null) return '';
  if (q.type === 'number') return String(a).replace(/[^0-9.,\\-]/g, '').slice(0, 12);
  if (q.type === 'slots' || q.type === 'sort') return a.map(x => (x === null || x === undefined) ? 'x' : String(x)).join('');
  return a.join('');
}

function decodeAnswer(q, s) {
  s = s || '';
  if (q.type === 'number') return s === '' ? null : s;
  if (s === '') return null;
  const parts = s.split('');
  if (q.type === 'slots' || q.type === 'sort') return parts.map(c => c === 'x' ? null : Number(c));
  return parts.map(Number);
}

function gradeFor(score) {
  return QUIZ.grades.find(g => score >= g.min) || QUIZ.grades[QUIZ.grades.length - 1];
}

