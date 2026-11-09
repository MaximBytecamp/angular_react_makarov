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
      "text": "После сборки готовую папку <code>dist</code> передали пользователю. Нужен ли ему Node.js, чтобы открыть приложение через веб-сервер? Выберите один вариант.",
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
      "code": "const finishFirst = () => {\n  requests[0].status = 'Готово'\n  setRequests(requests)\n}",
      "file": "App.tsx"
    },
    {
      "id": "q11",
      "topic": "1.6 · управляемая форма",
      "type": "multi",
      "text": "Поле названия заявки управляется React. Что обязательно связывает поле с состоянием? Отметьте все верные варианты.",
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

