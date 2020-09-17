import datetime
import sqlalchemy
import sqlalchemy.orm

import tables
import tables.twsedaily
import tables.fetched_date
import tables.transaction_history


class SqliteAdapter:
    def __init__(self, db_conf: dict):
        db_string = f"sqlite:///{db_conf['location']}"
        engine = sqlalchemy.create_engine(db_string)
        session = sqlalchemy.orm.sessionmaker(engine)
        session.configure(bind=engine)
        self.session = session()
        tables.twsedaily.get_table(tables.base.metadata)
        tables.fetched_date.get_table(tables.base.metadata)
        tables.transaction_history.get_table(tables.base.metadata)
        tables.base.metadata.create_all(engine)

    def query_fetched_date(self):
        return [d.date for d in self.session.query(tables.fetched_date.FetchedDate).all()]

    def query_transaction_histories(self) -> [tables.transaction_history.TransactionHistory]:
        return self.session.query(tables.transaction_history.TransactionHistory).order_by(
            tables.transaction_history.TransactionHistory.date.desc()).all()

    def insert_daily_stocks(self, stock_data: list, fetched_date: datetime.date):
        self._insert_fetched_date(fetched_date, stock_data != [])
        self._insert_stocks(stock_data, fetched_date)

    def insert_transaction_histories(self, transaction_data: list):
        fetched_records = [tables.transaction_history.to_transaction_history(t) for t in transaction_data]
        old_records = self.session.query(tables.transaction_history.TransactionHistory).all()
        new_records = self._get_insertable_transaction_histories(fetched_records, old_records)
        if not new_records:
            return
        self.session.add_all(new_records)
        self.session.commit()
        self.session.flush()

    def _get_insertable_transaction_histories(
            self, new: [tables.transaction_history.TransactionHistory],
            old: [tables.transaction_history.TransactionHistory]) -> [tables.transaction_history.TransactionHistory]:
        d = {(r.commissionId, r.date): r for r in old}
        return list(filter(lambda x: (x.commissionId, x.date) not in d, new))

    def _insert_fetched_date(self, fetched_date: datetime.date, is_transaction_date: bool):
        record = tables.fetched_date.to_fetched_date(fetched_date, is_transaction_date)
        self.session.add(record)
        self.session.commit()
        self.session.flush()

    def _insert_stocks(self, stock_data: list, fetched_date: datetime.date):
        records = [tables.twsedaily.to_twse_daily(data, fetched_date) for data in stock_data]
        self.session.add_all(records)
        self.session.commit()
        self.session.flush()

    def query_stock_after_date(self, date: datetime.date):
        return self.session.query(tables.twsedaily.TwseDaily).filter(
            tables.twsedaily.TwseDaily.date > date).order_by(
            tables.twsedaily.TwseDaily.sid, tables.twsedaily.TwseDaily.date.desc()).all()

    def query_latest_stock(self):
        records = self.session.query(tables.twsedaily.TwseDaily).filter(
            tables.twsedaily.TwseDaily.date > datetime.date.today()).all()
        if records:
            return records
        else:
            return self.session.query(tables.twsedaily.TwseDaily).filter(
                tables.twsedaily.TwseDaily.date > datetime.date.today() + datetime.timedelta(days=-1)).all()


    def reset(self):
        self.session.query(tables.twsedaily.TwseDaily).delete()
        self.session.query(tables.fetched_date.FetchedDate).delete()
        self.session.commit()
        self.session.flush()
