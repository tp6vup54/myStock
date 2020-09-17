import asyncio
import configparser
import datetime
import logging
import logging.config
import os

import consumer.stock
import db.sqlite
import fetcher.id
import fetcher.stock


def init_logger():
    """
    Init logger. Default use INFO level. If 'DEBUG' is '1' in env use DEBUG level.
    :return:
    """
    logging.config.fileConfig("conf/logging.conf")
    root = logging.getLogger()
    level = logging.INFO
    if os.getenv("DEBUG") == '1':
        level = logging.DEBUG
    root.setLevel(level)


async def main():
    init_logger()
    config = configparser.ConfigParser()
    config.sections()
    config.read('conf/myStock.conf')
    stock_fetcher = fetcher.stock.StockFetcher()
    date = datetime.date.today() + datetime.timedelta(days=-7)
    sqlite = db.sqlite.SqliteAdapter(dict(config['SQLITE']))
    fetched_date = sqlite.query_fetched_date()
    await asyncio.wait(
        [stock_fetcher.request_all_stock_from_day(date, fetched_date),
         consumer.stock.consumer(stock_fetcher, sqlite)]
    )


asyncio.run(main())
