from enum import Enum


class TradingSignalActionEnum(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    IGNORE = "IGNORE"


class TradingSignalStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    CANCELED = "CANCELED"
