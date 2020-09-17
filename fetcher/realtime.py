import asyncio
import datetime
import logging
import requests
import time

import common.realtime


class RealtimeFetcher:
    def __init__(self):
        self.TWSE_REALTIME = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_id}&_={time}'
        self.date_queue = asyncio.Queue()

    def _request_task(self, stock_ids: [str]):
        def _join_stock_id(stocks) -> str:
            return '|'.join(['tse_{}.tw'.format(s) for s in stocks])
        rv = requests.get(self.TWSE_REALTIME.format(stock_id=_join_stock_id(stock_ids), time=int(time.time()) * 1000),
                          headers={'referer': 'mis.twse.com.tw'})
        return rv.json()['msgArray']

    async def request_realtime_by_stock_ids(self, stock_ids: [str]) -> [common.realtime.Realtime]:
        loop = asyncio.get_running_loop()
        stock_ids = stock_ids[:137] if len(stock_ids) > 137 else stock_ids
        while True:
            logging.info('%s realtime start query' % datetime.datetime.now().strftime('%H%M%S'))
            t = loop.run_in_executor(None, self._request_task, stock_ids)
            await self.date_queue.put(t)
            await asyncio.sleep(5)

    async def get_next_realtime_data(self) -> list:
        t = await self.date_queue.get()
        self.date_queue.task_done()
        data = await t
        if data:
            return data
        else:
            return []
