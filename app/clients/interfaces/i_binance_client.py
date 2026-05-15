class IBicnanceClient:
    def get_balance(self, asset: str):
        raise NotImplementedError

    def get_price(self, symbol: str):
        raise NotImplementedError

    def create_market_buy(self, symbol: str, quantity: float):
        raise NotImplementedError

    def create_market_sell(self, symbol: str, quantity: float):
        raise NotImplementedError

    def get_open_orders(self, symbol: str):
        raise NotImplementedError
