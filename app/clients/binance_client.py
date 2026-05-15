import os
from app.clients.interfaces.i_binance_client import IBicnanceClient
from app.core.config import get_settings
from binance.client import Client


class BinanceClient(IBicnanceClient):

    def __init__(self):
        settings = get_settings()
        self.client = Client(
            api_key=settings.BINANCE_API_KEY,
            api_secret=settings.BINANCE_API_SECRET,
        )

    def get_balance(self, asset: str):
        return self.client.get_asset_balance(asset=asset)

    def get_price(self, symbol: str):
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])

    def create_market_buy(self, symbol: str, quantity: float):
        return self.client.order_market_buy(symbol=symbol, quantity=quantity)

    def create_market_sell(self, symbol: str, quantity: float):
        return self.client.order_market_sell(symbol=symbol, quantity=quantity)

    def get_open_orders(self, symbol: str):
        return self.client.get_open_orders(symbol=symbol)


3
