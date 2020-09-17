import datetime


class Realtime:
    def __init__(self, sid: str, latest_trade_price: float, trade_volume: int, accumulate_trade_volume: int,
                 best_buy_price: [float], best_buy_volume: [int], best_sell_price: [float], best_sell_volume: [int],
                 open: float, high: float, low: float, time: datetime.datetime):
        self.sid = sid
        self.latest_trade_price = latest_trade_price
        self.trade_volume = trade_volume
        self.accumulate_trade_volume = accumulate_trade_volume
        self.best_buy_price = best_buy_price
        self.best_buy_volume = best_buy_volume
        self.best_sell_price = best_sell_price
        self.best_sell_volume = best_sell_volume
        self.open = open
        self.high = high
        self.low = low
        self.time = time


def _to_realtime(realtime_data: dict) -> Realtime:
    def _cast_with_default(s: str, t: type, default):
        try:
            return t(s)
        except:
            return default
    def _split_best(d: str, t: type):
        if d:
            return list(map(lambda x: _cast_with_default(x, t, 0), d.strip('_').split('_')))
        return d
    return Realtime(realtime_data.get('c'),
                    _cast_with_default(realtime_data.get('z', None), float, 0.0),
                    _cast_with_default(realtime_data.get('tv', None), int, 0),
                    _cast_with_default(realtime_data.get('v', None), int, 0),
                    _split_best(realtime_data.get('b', None), float),
                    _split_best(realtime_data.get('g', None), int),
                    _split_best(realtime_data.get('a', None), float),
                    _split_best(realtime_data.get('f', None), int),
                    _cast_with_default(realtime_data.get('o', None), float, 0.0),
                    _cast_with_default(realtime_data.get('h', None), float, 0.0),
                    _cast_with_default(realtime_data.get('l', None), float, 0.0),
                    datetime.datetime.fromtimestamp(int(realtime_data['tlong']) / 1000))
