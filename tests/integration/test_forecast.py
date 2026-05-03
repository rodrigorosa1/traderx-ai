from main import app
from app.core.injections import get_api_customer_service


def test_get_forecast_route(client):
    class StubApiCustomerService:
        def forecast(self, api_key, tickers, hours):
            assert api_key == "valid-api-key"
            assert tickers == ["BTC-USD", "ETH-USD"]
            assert hours == 24
            return {
                "timeframe": "1h",
                "horizon_hours": hours,
                "total_assets": len(tickers),
                "results": [
                    {
                        "asset": {
                            "name": "Bitcoin",
                            "symbol": "BTC-USD",
                            "code": "BTC",
                            "directional": "up",
                            "directional_percent_period": 1.5,
                        },
                        "reference_price": 100.0,
                        "reference_datetime": "2024-01-01 00:00:00",
                        "backtest": {
                            "windows_used": 3,
                            "horizon_hours": hours,
                            "mae": 1.0,
                            "rmse": 1.2,
                            "mape_percent": 1.1,
                            "directional_accuracy_percent": 75.0,
                            "quality_score_percent": 80.0,
                        },
                        "forecast": [
                            {
                                "datetime": "2024-01-01 01:00:00",
                                "target_price": 101.0,
                                "lower_bound_price": 99.0,
                                "upper_bound_price": 103.0,
                                "confidence_percent": 80.0,
                            }
                        ],
                        "error": None,
                    }
                ],
            }

    app.dependency_overrides[get_api_customer_service] = StubApiCustomerService

    try:
        response = client.get(
            "forecast/?tickers=BTC-USD,ETH-USD&hours=24",
            headers={"X-ChainProphet-Key": "valid-api-key"},
        )
    finally:
        app.dependency_overrides.pop(get_api_customer_service, None)

    assert response.status_code == 200

    data = response.json()
    assert data["timeframe"] == "1h"
    assert data["horizon_hours"] == 24
    assert data["total_assets"] == 2
    assert len(data["results"]) == 1
    assert data["results"][0]["asset"]["symbol"] == "BTC-USD"
