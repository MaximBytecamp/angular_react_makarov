import { useEffect, useState } from 'react'
import Header from './components/Header'
import RequestForm from './components/RequestForm'
import RequestCard from './components/RequestCard'
import { nextStatus, type NewRequest, type RequestItem, type Status } from './requests'
import { fetchRequests } from './api'
import { sendRequest } from './notify'

type Filter = 'Все' | Status

const FILTERS: Filter[] = ['Все', 'Новая', 'В работе', 'Готово']

function App() {
  const [requests, setRequests] = useState<RequestItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const [filter, setFilter] = useState<Filter>('Все')
  const [notice, setNotice] = useState('')

  const newCount = requests.filter((r) => r.status === 'Новая').length
  const visible = filter === 'Все' ? requests : requests.filter((r) => r.status === filter)

  useEffect(() => {
    let ignore = false
    async function load() {
      try {
        const list = await fetchRequests()
        if (!ignore) {
          setRequests(list)
        }
      } catch (e) {
        if (!ignore) {
          setError((e as Error).message)
        }
      }
      if (!ignore) {
        setLoading(false)
      }
    }
    load()
    return () => {
      ignore = true
    }
  }, [attempt])

  useEffect(() => {
    document.title = `Новых: ${newCount} · Доска заявок`
  }, [newCount])

  useEffect(() => {
    if (notice === '') {
      return
    }
    const timer = setTimeout(() => setNotice(''), 5000)
    return () => clearTimeout(timer)
  }, [notice])

  useEffect(() => {
    function handleKey(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        setFilter('Все')
      }
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [])

  function retry() {
    setError('')
    setLoading(true)
    setAttempt(attempt + 1)
  }

  function handleNext(id: string) {
    const updated = requests.map((r) => {
      if (r.id === id) {
        return { ...r, status: nextStatus(r.status) }
      }
      return r
    })
    setRequests(updated)
  }

  async function handleAdd(data: NewRequest) {
    const created: RequestItem = { ...data, id: String(Date.now()), status: 'Новая' }
    setRequests([created, ...requests])
    setNotice('Заявка добавлена. Отправляем уведомление…')
    const sent = await sendRequest(created)
    if (sent) {
      setNotice('Заявка добавлена, уведомление отправлено.')
    } else {
      setNotice('Заявка добавлена, но уведомление не отправлено: сервер автоматизации недоступен.')
    }
  }

  function handleRemove(id: string) {
    setRequests(requests.filter((r) => r.id !== id))
  }

  return (
    <>
      <Header newCount={newCount} />
      <main className="board">
        <RequestForm onAdd={handleAdd} />
        <section className="list">
          <h2>Заявки</h2>
          {notice !== '' && <p className="notice">{notice}</p>}
          <div className="filters">
            {FILTERS.map((f) => (
              <button key={f} className={f === filter ? 'active' : ''} onClick={() => setFilter(f)}>
                {f}
              </button>
            ))}
          </div>
          {loading && <p className="empty">Загрузка заявок…</p>}
          {error !== '' && (
            <div className="load-error">
              <p>{error}</p>
              <button onClick={retry}>Повторить</button>
            </div>
          )}
          {!loading && error === '' && visible.length === 0 && <p className="empty">Заявок с таким статусом нет</p>}
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
