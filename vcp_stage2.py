import configparser
import json

import common.alert
import db.sqlite
import strategy.stock


def get_stock_on_hand(sql: db.sqlite) -> [str]:
    transaction_histories = sql.query_transaction_histories()
    stock_ids = {}
    for t in transaction_histories:
        if t.sid in stock_ids:
            stock_ids[t.sid] += t.type
        else:
            stock_ids[t.sid] = t.type
    return [k for k, v in stock_ids.items() if v > 0]


config = configparser.ConfigParser()
config.sections()
config.read('conf/myStock.conf')
sqlite = db.sqlite.SqliteAdapter(dict(config['SQLITE']))
stock_strategy = strategy.stock.StockStrategy(sqlite)
stocks = sorted(stock_strategy.vcp_stage2(), key=lambda x: x.current_volume, reverse=True)
stocks_d = {s.sid: s for s in stocks}
with open('json/alert.json') as f:
    alerts = [common.alert.Alert(s['id'], s['price'], s['direction']) for s in json.load(f)]
stock_on_hand = get_stock_on_hand(sqlite)
for a in alerts:
    if a.sid in stocks_d:
        del stocks_d[a.sid]
for s in stock_on_hand:
    if s in stocks_d:
        del stocks_d[s]
stocks = list(stocks_d.values())
print('\n'.join(['%s    %s' % (s.sid, s.twse_dailys[0].close) for s in stocks]))
print('len = %d' % len(stocks))
