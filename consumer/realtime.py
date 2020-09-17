import json
import logging

import fetcher.realtime
import common.alert
import common.realtime
import common.stock
import strategy.realtime


async def consumer(realtime_fetcher: fetcher.realtime.RealtimeFetcher, stocks: [common.stock.Stock]):
    sd = {s.sid: s for s in stocks}
    realtime_strategy = strategy.realtime.RealtimeStrategy()
    alerts = []
    with open('json/alert.json') as f:
        alerts = [common.alert.Alert(s['id'], s['price'], s['direction']) for s in json.load(f)]
    while True:
        try:
            realtime_data = await realtime_fetcher.get_next_realtime_data()
            realtimes = [common.realtime._to_realtime(r) for r in realtime_data]
            logging.info('calculating...')
            for r in realtimes:
                if realtime_strategy.is_need_alert(alerts, r):
                    logging.info('%s    %s' % (r.sid, str(realtime_strategy.get_alert_price(alerts, r))))
        except Exception as e:
            logging.error(e)
