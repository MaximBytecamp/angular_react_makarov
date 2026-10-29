const zayavki = [
  { title: 'Нет интернета', room: '305', category: 'Интернет', details: 'На всех компьютерах в кабинете не открываются сайты.' },
  { title: 'Замятие бумаги в принтере', room: '112', category: 'Принтер', details: 'Принтер пишет «замятие бумаги», лоток пустой.' },
  { title: 'Не включается компьютер', room: '214', category: 'Компьютер', details: 'Компьютер преподавателя не реагирует на кнопку питания.' },
  { title: 'Не работает мышь', room: '118', category: 'Компьютер', details: 'Курсор не двигается, мышь подключена к компьютеру № 7.' },
]
for (const z of zayavki) {
  const response = await fetch('http://localhost:8090/api/collections/requests/records', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...z, status: 'Новая' }),
  })
  console.log(response.status, z.title)
}
