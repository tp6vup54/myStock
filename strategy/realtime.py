import common.alert
import common.realtime
import common.stock


class RealtimeStrategy:
    # not work
    def is_big_transaction(self, stock: common.stock.Stock, realtime: common.realtime.Realtime) -> bool:
        def bigger_than_20(x, y):
            return x - (20 if x <= 100 else x * 0.2) > y
        return stock.current_volume / 270 < realtime.trade_volume * 1000 \
               and stock.vol5[0] / 270 < realtime.trade_volume * 1000 \
               and stock.vol20[0] / 270 < realtime.trade_volume * 1000 \
               and sum(realtime.best_buy_volume) > sum(realtime.best_sell_volume) \
               and bigger_than_20(realtime.best_buy_volume[0], realtime.best_sell_volume[0])

    def is_need_alert(self, alerts: [common.alert.Alert], realtime: common.realtime.Realtime) -> bool:
        d = {a.sid: a for a in alerts}
        sid = realtime.sid
        if sid in d:
            return d.get(sid).verify_alert(realtime)
        else:
            return False

    def get_alert_price(self, alerts: [common.alert.Alert], realtime: common.realtime.Realtime):
        d = {a.sid: a for a in alerts}
        return d.get(realtime.sid).price
