import asyncio
import datetime
import logging
import requests


def filter_stock_by_stock_id(stock_dict: dict, stock_ids: [str]) -> list:
    filtered_stock_data = []
    for stock_id in stock_ids:
        stock_data = stock_dict.get(stock_id)
        if stock_data:
            filtered_stock_data.append(stock_data)
    return filtered_stock_data


class StockFetcher:
    def __init__(self):
        self.TWSE_STOCK_DATA_URL = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALL'
        self.date_queue = asyncio.Queue()

    def _request_task(self, current_date: datetime.date):
        rv = requests.get(self.TWSE_STOCK_DATA_URL % current_date.strftime('%Y%m%d'))
        raw_json = rv.json()
        if 'data9' not in raw_json:
            return current_date, {}
        stock_json = raw_json['data9']
        stock_dict = {}
        for stock in stock_json:
            stock_dict[stock[0]] = stock
        return current_date, stock_dict

    async def request_all_stock_from_day(self, date: datetime.date, fetched_dates: [datetime.date]):
        loop = asyncio.get_running_loop()
        current_date = date
        while current_date <= datetime.date.today():
            if self._is_need_to_ignored(current_date, fetched_dates):
                current_date += datetime.timedelta(days=1)
                continue
            logging.info('%s stock data start query' % current_date.strftime('%Y%m%d'))
            t = loop.run_in_executor(None, self._request_task, current_date)
            await self.date_queue.put(t)
            current_date += datetime.timedelta(days=1)
            await asyncio.sleep(3)
        await self.date_queue.put(None)

    def _is_need_to_ignored(self, current_date: datetime.date, fetched_dates: [datetime.date]):
        if current_date in fetched_dates:
            logging.info('%s was fetched before, skip' % current_date.strftime('%Y%m%d'))
            return True
        if current_date == datetime.date.today() and datetime.datetime.now().time() < datetime.time(13, 45):
            logging.info('Stock market is not close yet, skip')
            return True
        return False

    async def get_next_stock_data(self) -> (datetime.date, dict):
        t = await self.date_queue.get()
        self.date_queue.task_done()
        data = await t
        if data:
            return data
        else:
            return (None, None)
