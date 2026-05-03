import unittest
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.schemas.user_schema import UserOut
from app.services.api_customer_service import ApiCustomerService


class TestApiCustomerService(unittest.TestCase):
    def _service(self, user_repository, history_repository, forecast_service):
        return ApiCustomerService(
            forecast_service=forecast_service,
            market_data_service=Mock(),
            sentiment_service=Mock(),
            signal_engine_service=Mock(),
            backtest_service=Mock(),
            user_repository=user_repository,
            history_repository=history_repository,
            ml_forecast_service=Mock(),
        )

    def test_forecast_success(self):
        user = UserOut(
            id=uuid4(),
            name="Anakin Skywalker",
            email="anakin.skywalker@jedi.com",
            phone="5548984863711",
            api_key="W8R9KcQe4ZP0xD7YH1nT2bM5aFJ6L9S",
            provider_customer_id=None,
            active=True,
        )
        forecast_result = {
            "timeframe": "1h",
            "horizon_hours": 24,
            "total_assets": 1,
            "results": [],
        }

        user_repository = Mock()
        user_repository.find_by_api_key.return_value = user

        history_repository = Mock()

        forecast_service = Mock()
        forecast_service.forecast_prices.return_value = forecast_result

        service = self._service(user_repository, history_repository, forecast_service)
        result = service.forecast(
            api_key=user.api_key, tickers=["BTC-USD"], hours=24
        )

        self.assertEqual(result, forecast_result)
        forecast_service.forecast_prices.assert_called_once_with(
            tickers=["BTC-USD"], hours=24
        )
        history_repository.create.assert_called_once_with(user_id=user.id)

    def test_forecast_error_invalid_api_key(self):
        user_repository = Mock()
        user_repository.find_by_api_key.return_value = None

        service = self._service(user_repository, Mock(), Mock())

        with pytest.raises(ValueError) as exc_info:
            service.forecast(api_key="invalid-key", tickers=["BTC-USD"], hours=24)

        assert str(exc_info.value) == "Invalid or inactive API key."

    def test_forecast_error_inactive_user(self):
        user = UserOut(
            id=uuid4(),
            name="Anakin Skywalker",
            email="anakin.skywalker@jedi.com",
            phone="5548984863711",
            api_key="W8R9KcQe4ZP0xD7YH1nT2bM5aFJ6L9S",
            provider_customer_id=None,
            active=False,
        )

        user_repository = Mock()
        user_repository.find_by_api_key.return_value = user

        service = self._service(user_repository, Mock(), Mock())

        with pytest.raises(ValueError) as exc_info:
            service.forecast(api_key=user.api_key, tickers=["BTC-USD"], hours=24)

        assert str(exc_info.value) == "Invalid or inactive API key."
