import type { RequestItem } from './requests'

const API_URL = 'http://localhost:8090/api/collections/requests/records'

async function callApi(url: string, options?: RequestInit): Promise<Response> {
  let response: Response
  try {
    response = await fetch(url, options)
  } catch {
    throw new Error('Сервер заявок не отвечает. Проверьте, что PocketBase запущен.')
  }
  if (!response.ok) {
    throw new Error(`Сервер отклонил запрос: код ${response.status}.`)
  }
  return response
}

export async function fetchRequests(): Promise<RequestItem[]> {
  const response = await callApi(`${API_URL}?sort=-created`)
  const data = await response.json()
  return data.items
}
