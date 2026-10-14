import { useState } from 'react'

type Status = 'Новая' | 'В работе' | 'Готово'

type RequestCardProps = {
  title: string
  room: string
  details: string
  status?: Status
}

function RequestCard({ title, room, details, status = 'Новая' }: RequestCardProps) {
  const [current, setCurrent] = useState(status)

  function handleClick() {
    if (current === 'Новая') {
      setCurrent('В работе')
    } else {
      setCurrent('Готово')
    }
  }

  return (
    <article className="card">
      <div className="card__top">
        <span className="card__room">каб. {room}</span>
        <span className="card__status">{current}</span>
      </div>
      <h3>{title}</h3>
      <p>{details}</p>
      <button onClick={handleClick} disabled={current === 'Готово'}>
        {current === 'Новая' ? 'Взять в работу' : 'Завершить'}
      </button>
    </article>
  )
}

export default RequestCard
