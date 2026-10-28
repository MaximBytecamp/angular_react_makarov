import { useState } from 'react'
import Header from './components/Header'
import RequestForm from './components/RequestForm'
import RequestCard from './components/RequestCard'
import { initialRequests, nextStatus } from './requests'

function App() {
  const [requests, setRequests] = useState(initialRequests)

  const newCount = requests.filter((r) => r.status === 'Новая').length

  function handleNext(id: number) {
    const updated = requests.map((r) => {
      if (r.id === id) {
        return { ...r, status: nextStatus(r.status) }
      }
      return r
    })
    setRequests(updated)
  }

  function handleRemove(id: number) {
    setRequests(requests.filter((r) => r.id !== id))
  }

  return (
    <>
      <Header newCount={newCount} />
      <main className="board">
        <RequestForm />
        <section className="list">
          <h2>Заявки</h2>
          {requests.length === 0 && <p className="empty">Заявок нет</p>}
          {requests.map((r) => (
            <RequestCard
              key={r.id}
              title={r.title}
              room={r.room}
              details={r.details}
              status={r.status}
              onNext={() => handleNext(r.id)}
              onRemove={() => handleRemove(r.id)}
            />
          ))}
        </section>
      </main>
    </>
  )
}

export default App
