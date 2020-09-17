import datetime
from sqlalchemy import Table, Column, Date, Boolean

from db.tables import base


class FetchedDate(base):
    __tablename__ = 'fetchedDate'
    __table_args__ = {'extend_existing': True}
    date = Column(Date, primary_key=True)
    is_transaction_date = Column(Boolean)


def get_table(meta) -> Table:
    return Table(FetchedDate.__tablename__, meta,
                 Column('date', Date, primary_key=True),
                 Column('is_transaction_date', Boolean))


def to_fetched_date(date: datetime.date, is_transaction_date: bool) -> FetchedDate:
    return FetchedDate(date=date, is_transaction_date=is_transaction_date)
