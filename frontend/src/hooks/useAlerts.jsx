import { useEffect, useState, useRef } from 'react'
import { fetchAlerts } from '../api/alerts'

export default function useAlerts(pollIntervalMs = 15 * 60 * 1000) {
  const [alerts, setAlerts] = useState({ active: false, areas: [] })
  const mounted = useRef(true)

  useEffect(() => {
    mounted.current = true
    let timer = null

    async function poll() {
      try {
        const data = await fetchAlerts()
        if (mounted.current) setAlerts(data)
      } catch (e) {
        // ignore errors; keep previous state
      }
    }

    poll()
    timer = setInterval(poll, pollIntervalMs)
    return () => {
      mounted.current = false
      if (timer) clearInterval(timer)
    }
  }, [pollIntervalMs])

  return alerts
}
