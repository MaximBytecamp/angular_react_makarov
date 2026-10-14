type RequestCardProps = {
  title: string
  room: string
  details: string
  status: string
}

function RequestCard({ title, room, details, status }: RequestCardProps) {
  return (
    <article className="card">
      <div className="card__top">
        <span className="card__room">каб. {room}</span>
        <span className="card__status">{status}</span>
      </div>
      <h3>{title}</h3>
      <p>{details}</p>
    </article>
  )
}

export default RequestCard
