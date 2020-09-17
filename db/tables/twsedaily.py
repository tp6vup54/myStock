import datetime
from sqlalchemy import Table, Column, String, Integer, Date, Float, BigInteger
from db.tables import base


class TwseDaily(base):
    __tablename__ = 'twseDaily'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    # 成交股數 (股)
    capacity = Column(BigInteger, nullable=False)
    # 成交筆數
    transaction = Column(BigInteger, nullable=False)
    # 成交金額 (新台幣/元)
    turnover = Column(BigInteger, nullable=False)
    # 開盤價
    open = Column(Float, nullable=False)
    # 最高價
    high = Column(Float, nullable=False)
    # 最低價
    low = Column(Float, nullable=False)
    # 收盤價
    close = Column(Float, nullable=False)
    # 漲跌價差
    change = Column(Float, nullable=False)


def get_table(meta) -> Table:
    return Table(TwseDaily.__tablename__, meta,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('sid', String, nullable=False, index=True),
                 Column('date', Date, nullable=False, index=True),
                 # 成交股數 (股)
                 Column('capacity', BigInteger, nullable=False),
                 # 成交筆數
                 Column('transaction', BigInteger, nullable=False),
                 # 成交金額 (新台幣/元)
                 Column('turnover', BigInteger, nullable=False),
                 # 開盤價
                 Column('open', Float, nullable=False),
                 # 最高價
                 Column('high', Float, nullable=False),
                 # 最低價
                 Column('low', Float, nullable=False),
                 # 收盤價
                 Column('close', Float, nullable=False),
                 # 漲跌價差
                 Column('change', Float, nullable=False))


def to_twse_daily(stock_data, date: datetime.date) -> TwseDaily:
    def safe_cast(val, to_type, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default
    return TwseDaily(sid=stock_data[0],
                     date=date,
                     capacity=safe_cast(stock_data[2].replace(',', ''), int, 0),
                     transaction=safe_cast(stock_data[3].replace(',', ''), int, 0),
                     turnover=safe_cast(stock_data[4].replace(',', ''), int, 0),
                     open=safe_cast(stock_data[5].replace(',', ''), float, 0.0),
                     high=safe_cast(stock_data[6].replace(',', ''), float, 0.0),
                     low=safe_cast(stock_data[7].replace(',', ''), float, 0.0),
                     close=safe_cast(stock_data[8].replace(',', ''), float, 0.0),
                     change=safe_cast(stock_data[10].replace(',', ''), float, 0.0))
