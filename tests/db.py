import datetime
import unittest

from db.sqlite import SqliteAdapter
from tables.twsedaily import TwseDaily


class TestDb(unittest.TestCase):
    def setUp(self):
        self.db = SqliteAdapter(
            {
                'database': 'stock',
                'user': 'sean',
                'password': 'yaya0102',
                'host': '127.0.0.1',
                'port': '5432'
            }
        )

    def tearDown(self):
        self.db.reset()

    def test_insert(self):
        record = TwseDaily(
            sid='0050',
            date=datetime.date.today(),
            capacity=12,
            transaction=23,
            turnover=333,
            open=1.1,
            high=2.2,
            low=1.0,
            close=1.1,
            change=0.1)
        self.db.insert_daily_stocks([record])
        stocks = self.db.query_stock_after_date('0050', datetime.date.today() + datetime.timedelta(days=-1))
        self.assertEqual(1, len(stocks))
        self.assertEqual('0050', stocks[0].sid)

    def test_select(self):
        record1 = TwseDaily(
            sid='0050',
            date=datetime.date.today(),
            capacity=12,
            transaction=23,
            turnover=333,
            open=1.1,
            high=2.2,
            low=1.0,
            close=1.1,
            change=0.1)
        record2 = TwseDaily(
            sid='0051',
            date=datetime.date.today(),
            capacity=12,
            transaction=23,
            turnover=333,
            open=1.1,
            high=2.2,
            low=1.0,
            close=1.1,
            change=0.1)
        record3 = TwseDaily(
            sid='0052',
            date=datetime.date.today(),
            capacity=12,
            transaction=23,
            turnover=333,
            open=1.1,
            high=2.2,
            low=1.0,
            close=1.1,
            change=0.1)
        self.db.insert_daily_stocks([record1, record2, record3])
        stocks = self.db.query_stock_after_date('0050', datetime.date.today() + datetime.timedelta(days=-1))
        self.assertEqual(1, len(stocks))
        self.assertEqual('0050', stocks[0].sid)


if __name__ == '__main__':
    unittest.main()
