import { useEffect, useState } from 'react'
import { fetchRequests } from './api'
import type { RequestItem } from './requests'

export function useRequests() {
  const [requests, setRequests] = useState<RequestItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)

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

  function retry() {
    setError('')
    setLoading(true)
    setAttempt(attempt + 1)
  }

  return { requests, setRequests, loading, error, retry }
}
