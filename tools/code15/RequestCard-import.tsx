import type { Status } from '../requests'

type RequestCardProps = {
  title: string
  room: string
  details: string
  status: Status
  onNext: () => void
}

function RequestCard({ title, room, details, status, onNext }: RequestCardProps) {
  return (
    <article className="card">
      <div className="card__top">
        <span className="card__room">каб. {room}</span>
        <span className="card__status">{status}</span>
      </div>
      <h3>{title}</h3>
      <p>{details}</p>
      <button onClick={onNext} disabled={status === 'Готово'}>
        {status === 'Новая' ? 'Взять в работу' : 'Завершить'}
      </button>
    </article>
  )
}

export default RequestCard
