import datetime

import common.stock
import db.sqlite
from strategy import multiple_filter


class StockStrategy:
    def __init__(self, db: db.sqlite.SqliteAdapter):
        self.db = db
        self.stocks = self._get_stocks()

    def _get_stocks(self) -> [common.stock.Stock]:
        stocks = self.db.query_stock_after_date(datetime.date.today() + datetime.timedelta(days=-365))
        return common.stock.to_stocks(stocks)

    def vcp_stage2(self) -> [common.stock.Stock]:
        filters = [
            lambda x: x.ma50[0] > x.ma150[0] if x.ma150 else True,
            lambda x: x.ma150[0] > x.ma200[0] if x.ma200 else True,
            lambda x: x.current_price > x.ma50[0] if x.ma50 else True,
            lambda x: x.continuous(x.ma200) > 22,
            lambda x: x.max_price_in_days(250) <= x.current_price * 1.25,
            lambda x: x.min_price_in_days(250) * 1.3 <= x.current_price,
            lambda x: x.vol5[0] > 50000,
        ]
        return list(multiple_filter(filters, self.stocks))
