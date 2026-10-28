const card = { id: 1, title: 'Не работает проектор', status: 'Новая' }
const copy = { ...card, status: 'В работе' }
console.log(card) // { id: 1, title: 'Не работает проектор', status: 'Новая' }
console.log(copy) // { id: 1, title: 'Не работает проектор', status: 'В работе' }
console.log(card === copy) // false
