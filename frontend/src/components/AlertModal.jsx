import React from 'react'

export default function AlertModal({ alerts, onClose }) {
  if (!alerts || !alerts.active) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-11/12 max-w-xl">
        <h2 className="text-xl font-bold mb-2">Weather Alert Details</h2>
        <p className="mb-4">Affected areas and reasons:</p>
        <ul className="list-disc pl-6 mb-4">
          {alerts.areas.map((a) => (
            <li key={a.area}>{a.area}: {a.reasons.join(', ')}</li>
          ))}
        </ul>
        <div className="text-right">
          <button onClick={onClose} className="px-4 py-2 bg-gray-200 rounded">Close</button>
        </div>
      </div>
    </div>
  )
}
