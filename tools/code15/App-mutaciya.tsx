import { useState } from 'react'
import Header from './components/Header'
import RequestForm from './components/RequestForm'
import RequestCard from './components/RequestCard'
import { initialRequests, nextStatus } from './requests'

function App() {
  const [requests, setRequests] = useState(initialRequests)

  const newCount = requests.filter((r) => r.status === 'Новая').length

  function handleNext(id: number) {
    const index = requests.findIndex((r) => r.id === id)
    requests[index].status = nextStatus(requests[index].status)
    console.log('Статус в массиве:', requests[index].status)
    setRequests(requests)
  }

  return (
    <>
      <Header newCount={newCount} />
      <main className="board">
        <RequestForm />
        <section className="list">
          <h2>Заявки</h2>
          {requests.map((r) => (
            <RequestCard
              key={r.id}
              title={r.title}
              room={r.room}
              details={r.details}
              status={r.status}
              onNext={() => handleNext(r.id)}
            />
          ))}
        </section>
      </main>
    </>
  )
}

export default App
