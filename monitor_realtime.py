import asyncio
import configparser
import logging
import logging.config
import os
import strategy

import common.stock
import consumer.realtime
import db.sqlite
import fetcher.realtime
import strategy.stock


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


def get_monitored_stocks() -> [common.stock.Stock]:
    config = configparser.ConfigParser()
    config.sections()
    config.read('conf/myStock.conf')
    sqlite = db.sqlite.SqliteAdapter(dict(config['SQLITE']))
    stock_strategy = strategy.stock.StockStrategy(sqlite)
    return sorted(stock_strategy.vcp_stage2(), key=lambda x: x.current_volume, reverse=True)


async def main():
    init_logger()
    stocks = get_monitored_stocks()
    realtime_fetcher = fetcher.realtime.RealtimeFetcher()
    await asyncio.wait([
        realtime_fetcher.request_realtime_by_stock_ids([
            s.sid for s in stocks]),
        consumer.realtime.consumer(realtime_fetcher, stocks)])


asyncio.run(main())
