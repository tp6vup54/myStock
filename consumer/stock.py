import logging

import db.sqlite
import fetcher.id
import fetcher.stock


async def consumer(stock_fetcher: fetcher.stock.StockFetcher, sqlite: db.sqlite.SqliteAdapter):
    id_fetcher = fetcher.id.StockIdFetcher()
    stock_ids = id_fetcher.get_stock_ids()
    while True:
        current_date, all_stock_data = await stock_fetcher.get_next_stock_data()
        if all_stock_data is None:
            break
        filtered_stock_data = fetcher.stock.filter_stock_by_stock_id(all_stock_data, stock_ids)
        try:
            sqlite.insert_daily_stocks(filtered_stock_data, current_date)
        except Exception as e:
            print(e)
        logging.info('%s stock data fetched and inserted' % current_date.strftime('%Y%m%d'))
