import { useState } from 'react'
import Header from './components/Header'
import RequestForm from './components/RequestForm'
import RequestCard, { type Status } from './components/RequestCard'

function nextStatus(status: Status): Status {
  if (status === 'Новая') {
    return 'В работе'
  }
  return 'Готово'
}

function App() {
  const [status1, setStatus1] = useState<Status>('Новая')
  const [status2, setStatus2] = useState<Status>('В работе')
  const [status3, setStatus3] = useState<Status>('Готово')

  const newCount = [status1, status2, status3].filter((s) => s === 'Новая').length

  return (
    <>
      <Header newCount={newCount} />
      <main className="board">
        <RequestForm />
        <section className="list">
          <h2>Заявки</h2>
          <RequestCard
            title="Не работает проектор"
            room="214"
            details="Проектор включается, но изображения на экране нет."
            status={status1}
            onNext={() => setStatus1(nextStatus(status1))}
          />
          <RequestCard
            title="Нет интернета"
            room="305"
            details="На всех компьютерах в кабинете не открываются сайты."
            status={status2}
            onNext={() => setStatus2(nextStatus(status2))}
          />
          <RequestCard
            title="Замятие бумаги в принтере"
            room="112"
            details="Принтер пишет «замятие бумаги», лоток пустой."
            status={status3}
            onNext={() => setStatus3(nextStatus(status3))}
          />
        </section>
      </main>
    </>
  )
}

export default App
