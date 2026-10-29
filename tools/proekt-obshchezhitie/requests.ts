export type Status = 'Новая' | 'В работе' | 'Готово'

export type Category = 'Сантехника' | 'Электрика' | 'Мебель' | 'Интернет'

export type RequestItem = {
  id: number
  title: string
  room: string
  category: Category
  details: string
  status: Status
}

export type NewRequest = {
  title: string
  room: string
  category: Category
  details: string
}

export const initialRequests: RequestItem[] = [
  {
    id: 1,
    title: 'Течёт кран в душевой',
    room: '214',
    category: 'Сантехника',
    details: 'Кран в душевой на втором этаже не закрывается до конца.',
    status: 'Новая',
  },
  {
    id: 2,
    title: 'Не работает розетка',
    room: '308',
    category: 'Электрика',
    details: 'Розетка у окна не работает, автомат в щитке включён.',
    status: 'В работе',
  },
  {
    id: 3,
    title: 'Сломан стул',
    room: '112',
    category: 'Мебель',
    details: 'У стула отломилась ножка.',
    status: 'Готово',
  },
  {
    id: 4,
    title: 'Нет Wi-Fi на этаже',
    room: '4 этаж',
    category: 'Интернет',
    details: 'Сеть общежития не видна с телефонов и ноутбуков.',
    status: 'Новая',
  },
  {
    id: 5,
    title: 'Не закрывается окно',
    room: '215',
    category: 'Мебель',
    details: 'Ручка окна прокручивается, створка не прижимается.',
    status: 'Новая',
  },
]

export function nextStatus(status: Status): Status {
  if (status === 'Новая') {
    return 'В работе'
  }
  return 'Готово'
}
