import { LocationForm } from '../components/LocationForm';
import { LocationList } from '../components/LocationList';
import useAlerts from '../hooks/useAlerts'
import AlertBanner from '../components/AlertBanner'
import AlertModal from '../components/AlertModal'
import { useState } from 'react'

export function Dashboard() {
  const alerts = useAlerts()
  const [showModal, setShowModal] = useState(false)

  return (
    <div className="min-h-screen">
      <AlertBanner alerts={alerts} onDismiss={() => setShowModal(false)} />
      {showModal && <AlertModal alerts={alerts} onClose={() => setShowModal(false)} />}

      <header className="border-b bg-white">
        <div className="mx-auto max-w-3xl px-4 py-4">
          <div>
            <h1 className="text-xl font-bold">Weather Starter</h1>
            <p className="text-sm text-slate-600">
              Stored snapshots; each location refreshes only when you trigger it.
            </p>
          </div>
        </div>
      </header>

      <main className="mx-auto grid max-w-3xl gap-4 px-4 py-6">
        <LocationForm />
        <LocationList />
      </main>
    </div>
  );
}
