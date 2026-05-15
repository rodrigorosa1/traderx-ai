from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional


class TradingStrategyService:
    MIN_CONFIDENCE_PERCENT = Decimal("70")
    MIN_EXPECTED_GAIN_PERCENT = Decimal("1.5")
    DEFAULT_STOP_LOSS_PERCENT = Decimal("1.5")
    DEFAULT_TAKE_PROFIT_PERCENT = Decimal("2.5")

    def analyze_forecasts(
        self, forecasts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        signals = []

        for forecast in forecasts:
            signal = self.analyze_single_forecast(forecast)

            if signal:
                signals.append(signal)

        return signals

    def analyze_single_forecast(
        self, forecast: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        asset = forecast.get("asset", {})

        symbol = asset.get("symbol") or asset.get("code")
        binance_symbol = self.to_binance_symbol(symbol)

        direction = forecast.get("direction")
        confidence_percent = self._to_decimal(forecast.get("confidence_percent"))
        expected_change_percent = self._to_decimal(
            forecast.get("expected_change_percent")
        )
        forecast_points = forecast.get("forecast", [])

        if not symbol:
            return None

        if not forecast_points:
            return self._build_signal(
                symbol=symbol,
                binance_symbol=binance_symbol,
                action="IGNORE",
                reason="missing_forecast_points",
                forecast=forecast,
            )

        if direction != "UP":
            return self._build_signal(
                symbol=symbol,
                binance_symbol=binance_symbol,
                action="IGNORE",
                reason="direction_not_up",
                forecast=forecast,
            )

        if confidence_percent < self.MIN_CONFIDENCE_PERCENT:
            return self._build_signal(
                symbol=symbol,
                binance_symbol=binance_symbol,
                action="IGNORE",
                reason="low_confidence",
                forecast=forecast,
                confidence_percent=confidence_percent,
                expected_change_percent=expected_change_percent,
            )

        if expected_change_percent < self.MIN_EXPECTED_GAIN_PERCENT:
            return self._build_signal(
                symbol=symbol,
                binance_symbol=binance_symbol,
                action="IGNORE",
                reason="low_expected_gain",
                forecast=forecast,
                confidence_percent=confidence_percent,
                expected_change_percent=expected_change_percent,
            )

        peak_point = self._find_peak_point(forecast_points)

        if not peak_point:
            return self._build_signal(
                symbol=symbol,
                binance_symbol=binance_symbol,
                action="IGNORE",
                reason="peak_point_not_found",
                forecast=forecast,
            )

        entry_price = self._to_decimal(forecast_points[0].get("estimated_price"))
        target_price = self._to_decimal(peak_point.get("estimated_price"))

        if entry_price <= 0 or target_price <= 0:
            return self._build_signal(
                symbol=symbol,
                binance_symbol=binance_symbol,
                action="IGNORE",
                reason="invalid_price",
                forecast=forecast,
            )

        stop_loss_price = entry_price * (
            Decimal("1") - self.DEFAULT_STOP_LOSS_PERCENT / Decimal("100")
        )

        take_profit_price = entry_price * (
            Decimal("1") + self.DEFAULT_TAKE_PROFIT_PERCENT / Decimal("100")
        )

        return {
            "symbol": symbol,
            "binance_symbol": binance_symbol,
            "action": "BUY",
            "status": "PENDING",
            "reason": "forecast_uptrend_detected",
            "confidence_percent": confidence_percent,
            "expected_change_percent": expected_change_percent,
            "entry_price": entry_price,
            "target_price": target_price,
            "take_profit_price": take_profit_price,
            "stop_loss_price": stop_loss_price,
            "target_datetime": self._parse_datetime(peak_point.get("datetime")),
            "forecast_snapshot": forecast,
        }

    def to_binance_symbol(self, symbol: Optional[str]) -> Optional[str]:
        if not symbol:
            return None

        return (
            symbol.upper()
            .replace("-USD", "USDT")
            .replace("-USDT", "USDT")
            .replace("-", "")
        )

    def _find_peak_point(
        self, forecast_points: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        valid_points = [
            point
            for point in forecast_points
            if point.get("estimated_price") is not None
        ]

        if not valid_points:
            return None

        return max(
            valid_points,
            key=lambda point: self._to_decimal(point.get("estimated_price")),
        )

    def _build_signal(
        self,
        symbol: str,
        binance_symbol: str,
        action: str,
        reason: str,
        forecast: Dict[str, Any],
        confidence_percent: Optional[Decimal] = None,
        expected_change_percent: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        return {
            "symbol": symbol,
            "binance_symbol": binance_symbol,
            "action": action,
            "status": "REJECTED" if action == "IGNORE" else "PENDING",
            "reason": reason,
            "confidence_percent": confidence_percent,
            "expected_change_percent": expected_change_percent,
            "forecast_snapshot": forecast,
        }

    def _to_decimal(self, value: Any) -> Decimal:
        if value is None:
            return Decimal("0")

        return Decimal(str(value))

    def _parse_datetime(self, value: Any):
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(
            tzinfo=None
        )
