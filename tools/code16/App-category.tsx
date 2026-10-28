import { useState } from 'react'
import Header from './components/Header'
import RequestForm from './components/RequestForm'
import RequestCard from './components/RequestCard'
import { initialRequests, nextStatus, type Status } from './requests'

type Filter = 'Все' | Status

const FILTERS: Filter[] = ['Все', 'Новая', 'В работе', 'Готово']

function App() {
  const [requests, setRequests] = useState(initialRequests)
  const [filter, setFilter] = useState<Filter>('Все')

  const newCount = requests.filter((r) => r.status === 'Новая').length
  const visible = filter === 'Все' ? requests : requests.filter((r) => r.status === filter)

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
          <div className="filters">
            {FILTERS.map((f) => (
              <button key={f} className={f === filter ? 'active' : ''} onClick={() => setFilter(f)}>
                {f}
              </button>
            ))}
          </div>
          {visible.length === 0 && <p className="empty">Заявок с таким статусом нет</p>}
          {visible.map((r) => (
            <RequestCard
              key={r.id}
              title={r.title}
              room={r.room}
              category={r.category}
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
