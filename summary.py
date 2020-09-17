import configparser

import common.statement
import db.sqlite

config = configparser.ConfigParser()
config.sections()
config.read('conf/myStock.conf')
sqlite = db.sqlite.SqliteAdapter(dict(config['SQLITE']))
latest_price = {s.sid: s.close for s in sqlite.query_latest_stock()}
transaction_records = sqlite.query_transaction_histories()
statement = common.statement.to_statement(transaction_records, latest_price)
print(statement.get_handover_profit_repr())
print(statement.get_in_stock_profit_repr())
print(statement.get_total_profit_repr())
print(statement.get_win_rate_repr())
