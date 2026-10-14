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
          <RequestCard
            title="Не работает проектор"
            room="214"
            details="Проектор включается, но изображения на экране нет."
            status="Новая"
          />
          <RequestCard
            title="Нет интернета"
            room="305"
            details="На всех компьютерах в кабинете не открываются сайты."
            status="В работе"
          />
          <RequestCard
            title="Замятие бумаги в принтере"
            room="112"
            details="Принтер пишет «замятие бумаги», лоток пустой."
            status="Готов"
          />
        </section>
      </main>
    </>
  )
}

export default App
