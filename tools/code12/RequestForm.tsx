function RequestForm() {
  return (
    <form className="form">
      <h2>Новая заявка</h2>

      <label htmlFor="title">Что случилось</label>
      <input id="title" type="text" placeholder="Например: не работает проектор" />

      <label htmlFor="room">Кабинет</label>
      <input id="room" type="text" placeholder="214" />

      <label htmlFor="category">Категория</label>
      <select id="category">
        <option>Компьютер</option>
        <option>Проектор</option>
        <option>Принтер</option>
        <option>Интернет</option>
      </select>

      <label htmlFor="details">Подробности</label>
      <textarea id="details" rows={3} />

      <button type="submit">Отправить заявку</button>
    </form>
  )
}

export default RequestForm
