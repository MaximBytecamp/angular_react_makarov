const list = await fetch('/api/collections/requests/records').then((r) => r.json())
await fetch('/api/collections/requests/records/' + list.items[0].id, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Чужое название' }),
}).then((r) => r.json())
