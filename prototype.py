import httpx

resp = httpx.get("https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast")
data = resp.json()

items = data.get("items", [])
if items:
    forecasts = items[0].get("forecasts", [])
    for f in forecasts:
        print(f.get("area"), f.get("forecast"))
