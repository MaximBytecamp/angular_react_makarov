/* Тест «Модуль 1 · компоненты, состояние и формы». Ключи и разбор обфусцированы в SECRET: это барьер от беглого чтения исходника, а не защита. */

const QUIZ = {
  "id": "angular-react-test-m1",
  "prefix": "AR1",
  "title": "Модуль 1 · компоненты, состояние и формы",
  "minutes": 35,
  "salt": "angular-react-m1-2026",
  "context": "Все задания опираются на главы 1.1–1.7 и автоматизацию модуля 1: доску заявок на React, сохранение в браузере и отправку заявки в n8n. Код приведён на TypeScript и JSX так же, как в справочнике.",
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
      "topic": "1.1 · Node.js и Vite",
      "type": "single",
      "text": "Готовая папка <code>dist</code> открывается через веб-сервер. Нужен ли для этого Node.js? Выберите один вариант.",
      "situation": { "title": "Ситуация", "facts": ["Выполнена команда <code>npm run build</code>.", "В папке <code>dist</code> появились HTML, CSS и JavaScript.", "Сайт открывается через веб-сервер."] },
      "image": { "svg": QUIZ_VIS.flow(["Исходники React", "npm run build", "Папка dist", "Браузер"], ["", "blue", "mint", ""]), "caption": "Путь проекта от исходников до браузера" },
      "options": [
        "Нет: готовые HTML, CSS и JavaScript выполняет браузер",
        "Да: Node.js выполняет компоненты React в браузере",
        "Да, но только для первого открытия приложения",
        "Нет, если вместе с dist передана папка node_modules"
      ]
    },
    {
      "id": "q02",
      "topic": "1.1 · файлы npm",
      "type": "sort",
      "text": "Разложите элементы проекта по их роли. Каждая карточка относится ровно к одной группе.",
      "image": { "src": "../../temy/11-node-npm-vite/img/09-provodnik-main.png", "alt": "Проводник VS Code с файлами React-проекта", "caption": "Файлы проекта после создания приложения через Vite" },
      "items": [
        "<code>package.json</code>",
        "<code>package-lock.json</code>",
        "<code>node_modules/</code>"
      ],
      "buckets": [
        "Нужные пакеты и команды проекта",
        "Точные версии всех зависимостей",
        "Скачанные файлы пакетов"
      ]
    },
    {
      "id": "q03",
      "topic": "1.2 · JSX",
      "type": "multi",
      "text": "Какие утверждения о JSX верны? Отметьте все верные варианты.",
      "options": [
        "Выражение JavaScript внутри разметки записывают в фигурных скобках",
        "Имя пользовательского компонента начинают с заглавной буквы",
        "Фрагмент <code>&lt;&gt;…&lt;/&gt;</code> не создаёт лишний элемент в браузере",
        "В JSX атрибут класса записывают как <code>class</code>",
        "Каждый экземпляр заявки должен быть отдельным компонентом с собственной разметкой"
      ]
    },
    {
      "id": "q04",
      "topic": "1.3 · props",
      "type": "slots",
      "text": "Компонент вызывают так: <code>&lt;RequestCard title=\"Не работает проектор\" room=\"214\" /&gt;</code>. Подставьте карточки в пропуски. Две карточки лишние.",
      "image": { "src": "../../temy/13-props/img/02-tri-zayavki.png", "alt": "Три карточки заявок с разными названиями и аудиториями", "caption": "Три экземпляра RequestCard получают разные значения props" },
      "chips": [
        "App",
        "RequestCard",
        "title",
        "room",
        "state",
        "onClick"
      ],
      "slots": [
        "Родительский компонент задаёт props",
        "Дочерний компонент получает props",
        "Значение «Не работает проектор» лежит в свойстве",
        "Значение «214» лежит в свойстве"
      ]
    },
    {
      "id": "q05",
      "topic": "1.4 · обработчик события",
      "type": "single",
      "text": "Кнопка должна вызвать <code>handleClick</code> только после нажатия. Какая запись правильная?",
      "situation": { "title": "Что происходит", "facts": ["Страница только открылась — обработчик ещё не нужен.", "Пользователь нажимает кнопку «Дальше».", "После нажатия должен выполниться <code>handleClick</code>."] },
      "options": [
        "<code>&lt;button onClick={handleClick}&gt;Дальше&lt;/button&gt;</code>",
        "<code>&lt;button onClick={handleClick()}&gt;Дальше&lt;/button&gt;</code>",
        "<code>&lt;button onClick=\"handleClick\"&gt;Дальше&lt;/button&gt;</code>",
        "<code>&lt;button click={handleClick}&gt;Дальше&lt;/button&gt;</code>"
      ]
    },
    {
      "id": "q06",
      "topic": "1.4 · useState",
      "type": "order",
      "text": "Пользователь нажал кнопку, обработчик вызвал функцию изменения состояния. Расставьте события в порядке, в котором React обновляет экран.",
      "image": { "svg": QUIZ_VIS.compare("ДО НАЖАТИЯ", ["Статус: Новая", "Счётчик: 1"], "ПОСЛЕ НАЖАТИЯ", ["Статус: Готово", "Счётчик: 0"]), "caption": "Два состояния интерфейса до и после события" },
      "items": [
        "Браузер сообщает React о нажатии",
        "React вызывает обработчик кнопки",
        "Обработчик вызывает функцию изменения состояния",
        "React повторно вызывает функцию компонента",
        "Компонент получает новое значение состояния и возвращает новую разметку"
      ]
    },
    {
      "id": "q07",
      "topic": "1.4 · подъём состояния",
      "type": "single",
      "text": "Шапке нужен счётчик новых заявок, а карточки меняют их статусы. Где хранить статусы, чтобы шапка и карточки видели согласованные данные?",
      "image": { "svg": QUIZ_VIS.tree("App", ["Header: счётчик", "RequestList", "RequestCard: статус"]), "caption": "Компоненты, которым нужны одни данные о заявках" },
      "options": [
        "В ближайшем общем родителе — компоненте App",
        "Отдельно в каждой карточке и отдельно в Header",
        "В обычной переменной внутри Header",
        "В CSS-классе каждой карточки"
      ]
    },
    {
      "id": "q08",
      "topic": "1.5 · map и filter",
      "type": "slots",
      "text": "Сопоставьте задачу с методом массива. Карточки можно использовать по одному разу.",
      "chips": [
        "map",
        "filter",
        "push",
        "sort"
      ],
      "slots": [
        "Построить карточку JSX для каждой заявки",
        "Оставить только заявки со статусом «Новая»"
      ]
    },
    {
      "id": "q09",
      "topic": "1.5 · key и неизменяемость",
      "type": "multi",
      "text": "Список заявок может удаляться, пополняться и сортироваться. Какие решения верны? Отметьте все верные варианты.",
      "situation": { "title": "Изменения списка", "facts": ["Новая заявка добавляется в начало.", "Готовую заявку можно удалить.", "Оставшиеся карточки меняют позиции после сортировки."] },
      "options": [
        "Использовать <code>request.id</code> как <code>key</code> карточки",
        "При изменении статуса построить новый массив через <code>map</code>",
        "Передать в <code>setRequests</code> тот же массив после изменения его элемента",
        "Использовать индекс массива как постоянный ключ заявки",
        "Хранить отфильтрованный список в отдельном состоянии и обновлять вручную"
      ]
    },
    {
      "id": "q10",
      "topic": "1.5 · обновление массива",
      "type": "line",
      "text": "Код должен перевести первую заявку в статус «Готово», но страница не обновляется. Нажмите строку, из-за которой React получает тот же массив.",
      "image": { "src": "../../temy/15-spiski-i-usloviya/img/07-mutaciya.png", "alt": "Код с прямым изменением элемента массива заявок", "caption": "Прямое изменение массива из главы о списках" },
      "code": "const finishFirst = () => {\n  requests[0].status = 'Готово'\n  setRequests(requests)\n}",
      "file": "App.tsx"
    },
    {
      "id": "q11",
      "topic": "1.6 · управляемая форма",
      "type": "multi",
      "text": "Поле названия заявки управляется React. Что обязательно связывает поле с состоянием? Отметьте все верные варианты.",
      "image": { "src": "../../temy/16-formy/img/04-controlled-nabrano.png", "alt": "Форма заявки с введённым названием", "caption": "Значение поля формы отражает состояние компонента" },
      "options": [
        "<code>value={title}</code> показывает значение состояния",
        "<code>onChange</code> записывает введённый текст в состояние",
        "<code>placeholder</code> сохраняет введённый текст",
        "<code>name</code> автоматически создаёт useState"
      ]
    },
    {
      "id": "q12",
      "topic": "1.6 · отправка формы",
      "type": "single",
      "text": "Форма должна добавлять заявку и по кнопке, и по Enter без перезагрузки страницы. Какое решение соответствует материалу?",
      "situation": { "title": "Проверка формы", "facts": ["Кнопка «Добавить» отправляет введённые данные.", "Клавиша Enter должна выполнять то же действие.", "Список и состояние приложения должны сохраниться без перезагрузки."] },
      "options": [
        "Обработчик <code>onSubmit</code> у формы и <code>event.preventDefault()</code>",
        "Обработчик <code>onClick</code> у div вокруг формы",
        "Обработчик <code>onChange</code> у кнопки",
        "Обычный <code>action</code> формы без обработчика React"
      ]
    },
    {
      "id": "q13",
      "topic": "1.7 · localStorage",
      "type": "order",
      "text": "После открытия страницы нужно восстановить сохранённые заявки. Расставьте действия по порядку.",
      "items": [
        "Прочитать строку из <code>localStorage</code>",
        "Если строки нет, вернуть начальный список",
        "Если строка есть, выполнить <code>JSON.parse</code>",
        "Передать функцию загрузки в <code>useState</code>"
      ]
    },
    {
      "id": "q14",
      "topic": "1.7 · запрос на вебхук",
      "type": "slots",
      "text": "Сопоставьте части запроса <code>sendRequest</code> с их назначением. Две карточки лишние.",
      "image": { "svg": QUIZ_VIS.flow(["Форма React", "fetch POST", "Webhook n8n", "Telegram"], ["", "blue", "", "mint"]), "caption": "Передача новой заявки во внешнюю автоматизацию" },
      "chips": [
        "POST",
        "application/json",
        "JSON.stringify(request)",
        "GET",
        "text/html"
      ],
      "slots": [
        "Метод отправки новой заявки",
        "Формат тела в заголовке Content-Type",
        "Преобразование объекта заявки в текст"
      ]
    },
    {
      "id": "q15",
      "topic": "1.8 · n8n и Telegram",
      "type": "multi",
      "text": "Доска отправляет заявку в n8n, а n8n — в Telegram. Какие утверждения верны? Отметьте все верные варианты.",
      "situation": { "title": "Система модуля", "facts": ["React отправляет объект заявки на Production URL вебхука.", "n8n формирует сообщение и вызывает Telegram Bot API.", "Доска опубликована на отдельном адресе."] },
      "image": { "src": "../../temy/18-avtomatizaciya/img/a07-canvas.png", "alt": "Схема процесса n8n с Webhook и Telegram", "caption": "Процесс n8n из автоматизации первого модуля" },
      "options": [
        "Токен бота хранят в n8n, а не в коде доски",
        "Production URL работает после публикации процесса",
        "Allowed Origins разрешает запросы с адреса доски",
        "Без тома Docker настройки n8n могут потеряться вместе с контейнером",
        "Test URL всегда работает после закрытия режима тестового ожидания"
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

