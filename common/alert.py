import common.realtime


class Alert:
    def __init__(self, sid: str, price: float, direction: int):
        self.operations = {
            1: lambda x: x >= self.price,
            -1: lambda x: x <= self.price
        }
        self.sid = sid
        self.price = price
        self.direction = direction

    def verify_alert(self, realtime: common.realtime.Realtime):
        return self.operations.get(self.direction)(realtime.best_sell_price[0])
