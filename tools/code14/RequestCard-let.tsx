type Status = 'Новая' | 'В работе' | 'Готово'

type RequestCardProps = {
  title: string
  room: string
  details: string
  status?: Status
}

function RequestCard({ title, room, details, status = 'Новая' }: RequestCardProps) {
  let current = status

  function handleClick() {
    current = 'В работе'
    console.log('current =', current)
  }

  return (
    <article className="card">
      <div className="card__top">
        <span className="card__room">каб. {room}</span>
        <span className="card__status">{current}</span>
      </div>
      <h3>{title}</h3>
      <p>{details}</p>
      <button onClick={handleClick}>Взять в работу</button>
    </article>
  )
}

export default RequestCard
