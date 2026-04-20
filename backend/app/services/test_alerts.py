from app.services.alerts import evaluate_area_alert, aggregate_alerts


def test_evaluate_area_alert_aqi():
    res = evaluate_area_alert("Central", 160, 0.0)
    assert "aqi" in res["reasons"]


def test_evaluate_area_alert_rain():
    res = evaluate_area_alert("North", None, 12.5)
    assert "heavy_rain" in res["reasons"]


def test_aggregate_alerts():
    areas = [
        {"area": "A", "reasons": ["aqi"]},
        {"area": "B", "reasons": []},
        {"area": "C", "reasons": ["heavy_rain"]},
    ]
    state = aggregate_alerts(areas, min_areas=2)
    assert state["active"] is True
    assert state["count"] == 2
