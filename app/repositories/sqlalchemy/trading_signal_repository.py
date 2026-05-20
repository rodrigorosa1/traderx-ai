from typing import Dict, List

from sqlalchemy.orm import Session

from app.constants.enums.trading_signal_enum import TradingSignalStatusEnum
from app.models.trading_signal import TradingSignal
from app.repositories.protocols.itrading_signal_repository import (
    ITradingSignalRepository,
)
from app.schemas.trading_signal_schema import TradingSignalOut


class TradingSignalRepository(ITradingSignalRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: Dict) -> TradingSignalOut:
        signal = TradingSignal(**data)

        self.db.add(signal)
        self.db.commit()
        self.db.refresh(signal)

        return signal

    def create_many(self, items: List[Dict]) -> List[TradingSignalOut]:
        signals = [TradingSignal(**item) for item in items]

        self.db.add_all(signals)
        self.db.commit()

        for signal in signals:
            self.db.refresh(signal)

        return signals

    def find_pending(self, limit: int = 100) -> List[TradingSignalOut]:
        return (
            self.db.query(TradingSignal)
            .filter(TradingSignal.status == TradingSignalStatusEnum.PENDING)
            .order_by(TradingSignal.created_at.asc())
            .limit(limit)
            .all()
        )

    def find_by_id(self, signal_id: int) -> TradingSignalOut | None:
        return (
            self.db.query(TradingSignal).filter(TradingSignal.id == signal_id).first()
        )
