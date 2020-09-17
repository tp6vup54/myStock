import datetime
from sqlalchemy import Table, Column, String, Integer, Date, Float, BigInteger
from db.tables import base


class TransactionHistory(base):
    __tablename__ = 'transactionHistory'
    __table_args__ = {'extend_existing': True}

    commissionId = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    sid = Column(String, nullable=False, index=True)
    # 成交股數 (股)
    capacity = Column(Integer, nullable=False)
    # 成交單價
    unitPrice = Column(Float, nullable=False)
    # 手續費
    handlingCharge = Column(Integer, nullable=False)
    # 交易稅
    tax = Column(Integer, nullable=False)
    # 現買 = 1/現賣 = -1
    type = Column(Integer, nullable=False)


def get_table(meta) -> Table:
    return Table(TransactionHistory.__tablename__, meta,
                 Column('commissionId', String, primary_key=True),
                 Column('date', Date, primary_key=True),
                 Column('sid', String, nullable=False, index=True),
                 # 成交股數 (股)
                 Column('capacity', Integer, nullable=False),
                 # 成交單價
                 Column('unitPrice', Float, nullable=False),
                 # 手續費
                 Column('handlingCharge', Integer, nullable=False),
                 # 交易稅
                 Column('tax', Integer, nullable=False),
                 # 現買 = 1/現賣 = -1
                 Column('type', Integer, nullable=False))


def to_transaction_history(data: list) -> TransactionHistory:
    types = {'現買': 1, '現賣': -1}
    return TransactionHistory(commissionId=data[-1],
                              date=datetime.datetime.strptime(data[0], '%Y/%m/%d').date(),
                              sid=data[2],
                              capacity=int(data[4].replace(',', '')),
                              unitPrice=float(data[5]),
                              handlingCharge=int(data[7]),
                              tax=int(data[8]),
                              type=types.get(data[1]))
