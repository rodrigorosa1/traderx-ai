from sqlalchemy import Column, DateTime, String, Numeric, JSON, Text
from app.constants.enums.trading_signal_enum import TradingSignalStatusEnum
from app.models.base import Base


class TradingSignal(Base):
    __tablename__ = "trading_signals"

    symbol = Column(String(30), nullable=False, index=True)
    binance_symbol = Column(String(30), nullable=False, index=True)

    action = Column(String(20), nullable=False)
    status = Column(
        String(20), nullable=False, default=TradingSignalStatusEnum.PENDING.value
    )

    reason = Column(String(100), nullable=False)

    confidence_percent = Column(Numeric(10, 4), nullable=True)
    expected_change_percent = Column(Numeric(10, 4), nullable=True)

    entry_price = Column(Numeric(24, 10), nullable=True)
    target_price = Column(Numeric(24, 10), nullable=True)
    take_profit_price = Column(Numeric(24, 10), nullable=True)
    stop_loss_price = Column(Numeric(24, 10), nullable=True)

    target_datetime = Column(DateTime, nullable=True)

    forecast_snapshot = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
