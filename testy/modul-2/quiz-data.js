/* Тест «Модуль 2 · эффекты, PocketBase и события». Ключи и разбор обфусцированы в SECRET: это барьер от беглого чтения исходника, а не защита. */

const QUIZ = {
  "id": "angular-react-test-m2",
  "prefix": "AR2",
  "title": "Модуль 2 · эффекты, PocketBase и события",
  "minutes": 35,
  "salt": "angular-react-m2-2026",
  "context": "Все задания опираются на главы 2.1–2.5, проект доски с базой и автоматизацию «ИИ-диспетчер». Ситуации относятся к той же доске заявок, PocketBase, n8n и Ollama из материалов модуля.",
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
      "topic": "2.1 · useEffect",
      "type": "multi",
      "text": "Какие утверждения о <code>useEffect</code> верны? Отметьте все верные варианты.",
      "situation": { "title": "Компонент Board", "facts": ["Компонент отрисовал список заявок.", "После отрисовки нужно подписаться на клавишу Esc.", "При удалении компонента подписку нужно снять."] },
      "image": { "svg": QUIZ_VIS.flow(["Рендер", "Эффект", "Подписка", "Очистка"], ["", "blue", "mint", "warn"]), "caption": "Жизненный цикл эффекта с внешней подпиской" },
      "options": [
        "Эффект выполняется после того, как React обновил экран",
        "<code>useEffect(f, [])</code> запускают при появлении компонента",
        "<code>useEffect(f, [x])</code> перезапускают при изменении x",
        "<code>useEffect(f)</code> выполняется только один раз",
        "Любое вычисляемое значение нужно хранить через эффект"
      ]
    },
    {
      "id": "q02",
      "topic": "2.1 · эффект или вычисление",
      "type": "sort",
      "text": "Разложите действия по месту, где они должны выполняться.",
      "image": { "svg": QUIZ_VIS.compare("ДАННЫЕ КОМПОНЕНТА", ["доступны в текущем вызове", "используются в JSX"], "ВНЕШНЯЯ СИСТЕМА", ["существует вне React", "требует синхронизации"]), "caption": "Данные компонента и внешняя система" },
      "items": [
        "Изменить <code>document.title</code>",
        "Поставить таймер и снять его при очистке",
        "Посчитать число новых заявок через <code>filter</code>",
        "Получить видимый список по выбранному фильтру"
      ],
      "buckets": [
        "В эффекте",
        "Обычное вычисление при отрисовке"
      ]
    },
    {
      "id": "q03",
      "topic": "2.1 · очистка эффекта",
      "type": "order",
      "text": "Эффект подписывается на клавишу Esc. Расставьте события жизненного цикла по порядку.",
      "image": { "svg": QUIZ_VIS.compare("ФОРМА НА ЭКРАНЕ", ["Esc закрывает форму", "обработчик активен"], "ФОРМЫ НЕТ", ["Esc не меняет экран", "обработчика нет"]), "caption": "Работа клавиши Esc при наличии и отсутствии формы" },
      "items": [
        "React обновляет экран с компонентом",
        "Эффект добавляет обработчик <code>keydown</code>",
        "Пользователь нажимает Esc, обработчик закрывает форму",
        "Компонент исчезает со страницы",
        "Функция очистки снимает обработчик"
      ]
    },
    {
      "id": "q04",
      "topic": "2.2 · PocketBase",
      "type": "sort",
      "text": "Сопоставьте элементы базы PocketBase с примерами из доски.",
      "image": { "src": "../../temy/22-pocketbase/img/12-records.png", "alt": "Таблица записей коллекции requests в PocketBase", "caption": "Коллекция requests и её записи в PocketBase" },
      "items": [
        "<code>requests</code>",
        "Заявка «Не работает проектор»",
        "<code>status</code>"
      ],
      "buckets": [
        "Коллекция",
        "Запись",
        "Поле"
      ]
    },
    {
      "id": "q05",
      "topic": "2.2 · правила API",
      "type": "single",
      "text": "В Delete rule записано <code>status = \"Готово\"</code>. Какое действие разрешает это правило?",
      "image": { "src": "../../temy/22-pocketbase/img/14-rules.png", "alt": "Поля правил доступа коллекции PocketBase", "caption": "Правила доступа коллекции requests" },
      "options": [
        "Удалять только записи, у которых в базе статус «Готово»",
        "Удалять любую запись и сразу менять её статус на «Готово»",
        "Удалять только поле status у готовой записи",
        "Удалять готовые записи только суперпользователю"
      ]
    },
    {
      "id": "q06",
      "topic": "2.3 · состояния загрузки",
      "type": "slots",
      "text": "Сопоставьте ситуацию интерфейса с состоянием списка.",
      "image": { "src": "../../temy/23-zagruzka/img/12-oshibka.png", "alt": "Экран ошибки загрузки с кнопкой Повторить", "caption": "Состояние интерфейса после неудачного запроса" },
      "chips": [
        "loading",
        "error",
        "data",
        "attempt",
        "ignore"
      ],
      "slots": [
        "Ответ сервера ещё не пришёл",
        "Ответ не придёт или сервер отказал",
        "Заявки получены и их можно показать"
      ]
    },
    {
      "id": "q07",
      "topic": "2.3 · fetch и 404",
      "type": "single",
      "text": "PocketBase ответил кодом 404. Почему <code>callApi</code> отдельно проверяет <code>response.ok</code>?",
      "options": [
        "fetch получил ответ и не отклоняет обещание из-за HTTP 404",
        "fetch всегда возвращает пустой массив при 404",
        "response.ok нужен только для преобразования JSON",
        "Без response.ok браузер повторит запрос бесконечно"
      ]
    },
    {
      "id": "q08",
      "topic": "2.3 · защита от старого ответа",
      "type": "single",
      "text": "В режиме разработки первый запуск эффекта уже очищен, но его запрос завершился позже второго. Что не даёт старому ответу перезаписать состояние?",
      "situation": { "title": "Два запроса", "facts": ["Запрос A начался первым.", "После очистки эффект запустил запрос B.", "B завершился раньше, а A вернулся последним."] },
      "image": { "svg": QUIZ_VIS.timeline(["A начался", "Очистка A", "B вернулся", "A вернулся поздно"], [1, 3]), "caption": "Старый запрос завершается после актуального" },
      "options": [
        "Флажок <code>ignore</code>, поднятый функцией очистки",
        "Поле <code>attempt</code> в PocketBase",
        "Компонент Header",
        "Метод <code>JSON.stringify</code>"
      ]
    },
    {
      "id": "q09",
      "topic": "2.3 · кнопка «Повторить»",
      "type": "single",
      "text": "В эффекте загрузки зависимость <code>attempt</code> напрямую не читается. Зачем она указана в массиве зависимостей?",
      "options": [
        "Её изменение после «Повторить» запускает эффект заново",
        "Она автоматически считает HTTP-запросы на сервере",
        "Она запрещает повторный запрос при ошибке",
        "Она хранит текст последней ошибки"
      ]
    },
    {
      "id": "q10",
      "topic": "2.3 · изменение после await",
      "type": "single",
      "text": "После <code>await updateRequest(...)</code> нужно изменить статус в списке, который за время ожидания мог обновиться. Какая форма безопаснее?",
      "situation": { "title": "Пока выполнялся запрос", "facts": ["Пользователь нажал «Взять».", "PocketBase обрабатывал изменение статуса.", "За это время подписка добавила в список новую заявку."] },
      "options": [
        "<code>setRequests((list) =&gt; list.map(...))</code>",
        "<code>setRequests(requests.map(...))</code>",
        "<code>requests[0].status = next</code>",
        "<code>setRequests(requests)</code>"
      ]
    },
    {
      "id": "q11",
      "topic": "2.4 · собственный хук",
      "type": "multi",
      "text": "Какие утверждения о <code>useRequests</code> верны? Отметьте все верные варианты.",
      "options": [
        "Имя собственного хука начинается с use",
        "Внутри собственного хука можно вызывать useState и useEffect",
        "Каждый компонент, вызвавший хук, получает своё состояние",
        "Один вызов хука автоматически делает состояние общим для всего приложения",
        "Хук можно вызывать после условного return"
      ]
    },
    {
      "id": "q12",
      "topic": "2.4 · порядок хуков",
      "type": "line",
      "text": "В компоненте нарушено правило неизменного порядка хуков. Нажмите строку, из-за которой при <code>hidden === true</code> хук не будет вызван.",
      "image": { "src": "../../temy/24-sobstvennyy-huk/img/10-ranniy-return.png", "alt": "Компонент с ранним return перед вызовом собственного хука", "caption": "Ранний выход меняет количество вызванных хуков" },
      "code": "function Board({ hidden }: Props) {\n  if (hidden) return null\n  const board = useRequests()\n  return <main>{board.requests.length}</main>\n}",
      "file": "Board.tsx"
    },
    {
      "id": "q13",
      "topic": "2.4 · два вызова хука",
      "type": "single",
      "text": "App и Header каждый отдельно вызвали <code>useRequests()</code>. App изменил статус заявки. Почему счётчик Header не изменился сразу?",
      "image": { "svg": QUIZ_VIS.tree("Два независимых вызова", ["App → useRequests", "Header → useRequests"]), "caption": "Каждый вызов собственного хука создаёт своё состояние" },
      "options": [
        "У каждого вызова хука свой список состояния",
        "Header не умеет читать props",
        "useRequests разрешено вызывать только в App",
        "PocketBase не поддерживает несколько запросов"
      ]
    },
    {
      "id": "q14",
      "topic": "2.5 · события сервера",
      "type": "sort",
      "text": "Распределите свойства между опросом и подпиской на события.",
      "image": { "src": "../../temy/25-obnovlenie-po-sobytiyam/img/13-eventstream.png", "alt": "Соединение EventStream в панели Network", "caption": "Открытое соединение для событий PocketBase" },
      "items": [
        "Браузер делает запрос раз в несколько секунд",
        "Большинство запросов может не принести изменений",
        "Сервер присылает сообщение в момент изменения",
        "Используется одно открытое соединение"
      ],
      "buckets": [
        "Опрос",
        "Подписка"
      ]
    },
    {
      "id": "q15",
      "topic": "2.5 и А2 · без дублей и ИИ-диспетчер",
      "type": "multi",
      "text": "Какие утверждения соответствуют доске модуля 2 и ИИ-диспетчеру? Отметьте все верные варианты.",
      "situation": { "title": "Автоматизация", "facts": ["PocketBase создаёт запись заявки.", "n8n передаёт текст локальной модели Ollama.", "Категория и кнопка «Взять» попадают в Telegram."] },
      "image": { "src": "../../temy/28-ii-dispetcher/img/b07-canvas-dispetcher.png", "alt": "Процесс n8n для ИИ-диспетчера заявок", "caption": "Процесс ИИ-диспетчера из второго модуля" },
      "options": [
        "<code>upsertRequest</code> не даёт задвоить заявку, пришедшую ответом POST и событием create",
        "Поле <code>format</code> задаёт JSON-схему ответа модели",
        "Нажатия кнопки Telegram опрашиваются через getUpdates, потому что локальный n8n не имеет публичного HTTPS-адреса",
        "Токен бота записывают прямо в шаблон процесса и передают этот файл вместе с проектом",
        "Исправленная в PocketBase категория останется только в окне с панелью администратора"
      ]
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

