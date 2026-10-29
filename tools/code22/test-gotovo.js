await fetch('/api/collections/requests/records', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Проверка правил', room: '101', category: 'Компьютер', status: 'Готово' }),
}).then((r) => r.json())
