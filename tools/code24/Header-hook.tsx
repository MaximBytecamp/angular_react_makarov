import { useRequests } from '../useRequests'

function Header() {
  const { requests } = useRequests()
  const newCount = requests.filter((r) => r.status === 'Новая').length

  return (
    <header className="header">
      <h1>Доска заявок</h1>
      <p>ИТ-отдел колледжа · заявки студентов и преподавателей</p>
      <span className="header__count">Новых заявок: {newCount}</span>
    </header>
  )
}

export default Header
