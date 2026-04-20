import React from 'react'

export default function AlertBanner({ alerts, onDismiss }) {
  if (!alerts || !alerts.active) return null

  const count = alerts.count || alerts.areas.length || 0

  return (
    <div className="bg-red-600 text-white p-4 fixed top-0 left-0 right-0 z-50">
      <div className="container mx-auto flex items-center justify-between">
        <div>
          <strong className="mr-2">Weather Alert</strong>
          {` — ${count} area(s) affected. Click for details.`}
        </div>
        <div>
          <button onClick={onDismiss} className="bg-red-800 px-3 py-1 rounded">Dismiss</button>
        </div>
      </div>
    </div>
  )
}
