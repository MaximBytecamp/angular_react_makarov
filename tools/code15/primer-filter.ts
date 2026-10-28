const statuses = ['Новая', 'В работе', 'Готово', 'Новая']
const onlyNew = statuses.filter((s) => s === 'Новая')
console.log(onlyNew) // [ 'Новая', 'Новая' ]
console.log(onlyNew.length) // 2
