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
      "code": "function Board({ hidden }: Props) {\n  if (hidden) return null\n  const board = useRequests()\n  return <main>{board.requests.length}</main>\n}",
      "file": "Board.tsx"
    },
    {
      "id": "q13",
      "topic": "2.4 · два вызова хука",
      "type": "single",
      "text": "App и Header каждый отдельно вызвали <code>useRequests()</code>. App изменил статус заявки. Почему счётчик Header не изменился сразу?",
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

