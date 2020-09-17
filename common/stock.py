import itertools

import db.tables.twsedaily


class Stock:
    def __init__(self, sid, twse_dailys: [db.tables.twsedaily.TwseDaily]):
        self.sid = sid
        self.twse_dailys = twse_dailys
        self.current_price = self.twse_dailys[0].close
        self.current_volume = self.twse_dailys[0].capacity
        self.ma50 = self._moving_average(50, lambda x: x.close)
        self.ma150 = self._moving_average(150, lambda x: x.close)
        self.ma200 = self._moving_average(200, lambda x: x.close)
        self.vol5 = self._moving_average(5, lambda x: x.capacity)
        self.vol20 = self._moving_average(20, lambda x: x.capacity)

    def _moving_average(self, days, property_lambda) -> [float]:
        result = []
        data = [property_lambda(twse) for twse in self.twse_dailys]
        for _ in range(len(data) - days + 1):
            result.append(round(sum(data[:days]) / days, 2))
            data = data[1:]
        return result

    def continuous(self, price: [float]) -> int:
        if not price:
            return 0
        diff = [1 if price[i] > price[i + 1] else -1 for i in range(0, len(price) - 1)]
        cont = 0
        for v in diff:
            if v == diff[0]:
                cont += 1
            else:
                break
        return cont * diff[0]

    def min_price_in_days(self, days):
        return min([s.close for s in self.twse_dailys[:days]])

    def max_price_in_days(self, days):
        return max([s.close for s in self.twse_dailys[:days]])


def to_stocks(twse_dailys: [[db.tables.twsedaily.TwseDaily]]):
    grouped_twse_dailys = itertools.groupby(twse_dailys, lambda x: x.sid)
    return [Stock(k, list(g)) for k, g in grouped_twse_dailys]
