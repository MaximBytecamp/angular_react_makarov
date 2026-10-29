export type Status = 'Новая' | 'В работе' | 'Готово'

export type Category = 'Компьютер' | 'Проектор' | 'Принтер' | 'Интернет'

export type RequestItem = {
  id: string
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

export function nextStatus(status: Status): Status {
  if (status === 'Новая') {
    return 'В работе'
  }
  return 'Готово'
}
