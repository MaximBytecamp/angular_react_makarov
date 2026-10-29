import { useState } from 'react'
import Header from './components/Header'
import RequestForm from './components/RequestForm'
import RequestCard from './components/RequestCard'
import { nextStatus, type NewRequest, type RequestItem, type Status } from './requests'
import { loadRequests, saveRequests } from './storage'

type Filter = 'Все' | Status

const FILTERS: Filter[] = ['Все', 'Новая', 'В работе', 'Готово']

function App() {
  const [requests, setRequests] = useState(loadRequests)
  const [filter, setFilter] = useState<Filter>('Все')

  const newCount = requests.filter((r) => r.status === 'Новая').length
  const visible = filter === 'Все' ? requests : requests.filter((r) => r.status === filter)

  function update(list: RequestItem[]) {
    setRequests(list)
    saveRequests(list)
  }

  function handleNext(id: number) {
    const updated = requests.map((r) => {
      if (r.id === id) {
        return { ...r, status: nextStatus(r.status) }
      }
      return r
    })
    update(updated)
  }

  function handleAdd(data: NewRequest) {
    const created: RequestItem = { ...data, id: Date.now(), status: 'Новая' }
    update([created, ...requests])
  }

  function handleRemove(id: number) {
    update(requests.filter((r) => r.id !== id))
  }

  return (
    <>
      <Header newCount={newCount} />
      <main className="board">
        <RequestForm onAdd={handleAdd} />
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
