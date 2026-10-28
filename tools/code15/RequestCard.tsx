import { useState } from 'react'
import type { Status } from '../requests'

type RequestCardProps = {
  title: string
  room: string
  details: string
  status: Status
  onNext: () => void
  onRemove: () => void
}

function RequestCard({ title, room, details, status, onNext, onRemove }: RequestCardProps) {
  const [open, setOpen] = useState(false)

  return (
    <article className="card">
      <div className="card__top">
        <span className="card__room">каб. {room}</span>
        <span className="card__status">{status}</span>
      </div>
      <h3>{title}</h3>
      {open && <p>{details}</p>}
      <div className="card__actions">
        <button className="card__more" onClick={() => setOpen(!open)}>
          {open ? 'Скрыть' : 'Подробнее'}
        </button>
        {status === 'Готово' ? (
          <button onClick={onRemove}>Убрать с доски</button>
        ) : (
          <button onClick={onNext}>{status === 'Новая' ? 'Взять в работу' : 'Завершить'}</button>
        )}
      </div>
    </article>
  )
}

export default RequestCard
