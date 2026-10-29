import json, time, urllib.request
SYSTEM = ("Ты диспетчер ИТ-отдела колледжа. По заявке определи категорию (Компьютер, Проектор, Принтер, Интернет), "
          "срочность и напиши краткое описание до 12 слов. Срочно — если не работает занятие или экзамен, "
          "пропал интернет у целого кабинета или есть риск для безопасности. Отвечай только JSON.")
SCHEMA = {"type": "object", "properties": {
    "category": {"type": "string", "enum": ["Компьютер", "Проектор", "Принтер", "Интернет"]},
    "urgent": {"type": "boolean"}, "summary": {"type": "string"}},
    "required": ["category", "urgent", "summary"]}
cases = [
 ("Не работает проектор", "214", "Проектор", "Через 10 минут экзамен, проектор не включается."),
 ("Нет интернета", "305", "Компьютер", "Во всём кабинете ни один компьютер не открывает сайты."),
 ("Замятие бумаги", "112", "Принтер", "Принтер пишет «замятие», лоток пустой. Не срочно."),
 ("Мышь заедает", "118", "Интернет", "Колёсико мыши иногда не крутится."),
 ("Из розетки искрит", "210", "Компьютер", "Розетка под компьютером искрит и пахнет гарью."),
 ("asdf", "1", "Компьютер", "ыва ыва"),
]
for t, room, cat, det in cases:
    body = {"model": "qwen2.5:3b", "stream": False, "format": SCHEMA,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": f"Что случилось: {t}\nКабинет: {room}\nКатегория от студента: {cat}\nПодробности: {det}"}]}
    s = time.time()
    req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
    out = json.load(urllib.request.urlopen(req, timeout=300))
    print(f"{time.time()-s:5.1f}s | {t} | {out['message']['content']}")
