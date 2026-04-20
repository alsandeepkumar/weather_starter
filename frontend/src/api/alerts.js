export async function fetchAlerts() {
  const res = await fetch('/api/alerts/');
  if (!res.ok) throw new Error('Failed to fetch alerts');
  return res.json();
}
