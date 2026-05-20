from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.constants.enums.trading_signal_enum import TradingSignalStatusEnum


class TradingSignalOut(BaseModel):
    id: UUID
    symbol: str
    binance_symbol: str
    action: str
    status: TradingSignalStatusEnum
    reason: Optional[str] = None
    confidence_percent: Optional[float] = None
    expected_change_percent: Optional[float] = None
    entry_price: Optional[float] = None
    target_price: Optional[float] = None
    take_profit_price: Optional[float] = None
    stop_loss_price: Optional[float] = None
    target_datetime: Optional[str] = None
    forecast_snapshot: Optional[dict] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
