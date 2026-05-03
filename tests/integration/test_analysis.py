from main import app
from app.core.injections import (
    get_forecast_evaluation_service,
    get_forecast_failure_classifier_service,
    get_forecast_langchain_analyst_service,
    get_forecast_llm_analyst_service,
    get_forecast_outcome_service,
    get_ml_training_service,
)


def test_collect_outcomes_route(client):
    class StubOutcomeService:
        def collect_pending_outcomes(self, limit=100):
            assert limit == 2
            return [{"forecast_point_id": "point-id"}]

    app.dependency_overrides[get_forecast_outcome_service] = StubOutcomeService

    try:
        response = client.post("analysis/collect-outcomes/?limit=2")
    finally:
        app.dependency_overrides.pop(get_forecast_outcome_service, None)

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Outcomes collected successfully"
    assert data["total_collected"] == 1
    assert data["items"] == [{"forecast_point_id": "point-id"}]


def test_evaluate_forecasts_route(client):
    class StubEvaluationService:
        def evaluate_pending_points(self, tolerance_percent=2.0, limit=100):
            assert tolerance_percent == 3.0
            assert limit == 2
            return [{"forecast_point_id": "point-id"}]

    app.dependency_overrides[get_forecast_evaluation_service] = StubEvaluationService

    try:
        response = client.post("analysis/evaluate?tolerance_percent=3.0&limit=2")
    finally:
        app.dependency_overrides.pop(get_forecast_evaluation_service, None)

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Forecasts evaluated successfully"
    assert data["total_evaluated"] == 1
    assert data["items"] == [{"forecast_point_id": "point-id"}]


def test_classify_failures_route(client):
    class StubClassifierService:
        def classify_pending_assets(self, limit=100):
            assert limit == 2
            return [{"forecast_asset_id": "asset-id"}]

    app.dependency_overrides[get_forecast_failure_classifier_service] = (
        StubClassifierService
    )

    try:
        response = client.post("analysis/classify-failures?limit=2")
    finally:
        app.dependency_overrides.pop(get_forecast_failure_classifier_service, None)

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Failures classified successfully"
    assert data["total_classified"] == 1
    assert data["items"] == [{"forecast_asset_id": "asset-id"}]


def test_llm_analyze_failures_route(client):
    class StubAnalystService:
        def analyze_pending_diagnostics(self, limit=20):
            assert limit == 2
            return [{"ai_report_id": "report-id"}]

    app.dependency_overrides[get_forecast_langchain_analyst_service] = (
        StubAnalystService
    )

    try:
        response = client.post("analysis/llm-analyze?limit=2")
    finally:
        app.dependency_overrides.pop(get_forecast_langchain_analyst_service, None)

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "AI reports generated successfully"
    assert data["total_generated"] == 1
    assert data["items"] == [{"ai_report_id": "report-id"}]


def test_llm_report_route(client):
    class StubLlmAnalystService:
        def list_reports(self, limit=50, offset=0):
            assert limit == 2
            assert offset == 1
            return [{"id": "report-id"}]

    app.dependency_overrides[get_forecast_llm_analyst_service] = StubLlmAnalystService

    try:
        response = client.post("analysis/llm-report?limit=2&offset=1")
    finally:
        app.dependency_overrides.pop(get_forecast_llm_analyst_service, None)

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["limit"] == 2
    assert data["offset"] == 1
    assert data["total_reports"] == 1
    assert data["items"] == [{"id": "report-id"}]


def test_train_ml_models_route(client):
    class StubTrainingService:
        def train_asset_models(self, ticker, horizon_hours):
            assert ticker == "BTC-USD"
            assert horizon_hours == 12
            return {"status": "success", "ticker": ticker, "horizon_hours": 12}

    app.dependency_overrides[get_ml_training_service] = StubTrainingService

    try:
        response = client.post("analysis/train-ml?ticker=btc-usd&hours=12")
    finally:
        app.dependency_overrides.pop(get_ml_training_service, None)

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["ticker"] == "BTC-USD"
    assert data["horizon_hours"] == 12
