import { useState } from 'react'
import type { Category } from '../requests'

function RequestForm() {
  const [title, setTitle] = useState('')
  const [room, setRoom] = useState('')
  const [category, setCategory] = useState<Category>('Компьютер')
  const [details, setDetails] = useState('')

  return (
    <form className="form">
      <h2>Новая заявка</h2>

      <label htmlFor="title">Что случилось</label>
      <input
        id="title"
        type="text"
        placeholder="Например: не работает проектор"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
      />

      <label htmlFor="room">Кабинет</label>
      <input
        id="room"
        type="text"
        placeholder="214"
        value={room}
        onChange={(event) => setRoom(event.target.value)}
      />

      <label htmlFor="category">Категория</label>
      <select
        id="category"
        value={category}
        onChange={(event) => setCategory(event.target.value as Category)}
      >
        <option>Компьютер</option>
        <option>Проектор</option>
        <option>Принтер</option>
        <option>Интернет</option>
      </select>

      <label htmlFor="details">Подробности</label>
      <textarea
        id="details"
        rows={3}
        value={details}
        onChange={(event) => setDetails(event.target.value)}
      />

      <p>
        Сейчас в состоянии: «{title}», каб. {room}, {category}
      </p>

      <button type="submit">Отправить заявку</button>
    </form>
  )
}

export default RequestForm
