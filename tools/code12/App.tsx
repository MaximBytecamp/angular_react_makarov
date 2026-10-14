import Header from './components/Header'
import RequestForm from './components/RequestForm'
import RequestCard from './components/RequestCard'

function App() {
  return (
    <>
      <Header />
      <main className="board">
        <RequestForm />
        <section className="list">
          <h2>Заявки</h2>
          <RequestCard />
          <RequestCard />
          <RequestCard />
        </section>
      </main>
    </>
  )
}

export default App
