import configparser

import db.sqlite
import google_sheet


config = configparser.ConfigParser()
config.sections()
config.read('conf/myStock.conf')
sqlite = db.sqlite.SqliteAdapter(dict(config['SQLITE']))
sheet_id = config['GOOGLE_SHEET']['sheet_id']
adapter = google_sheet.GoogleSheetAdapter()
records = adapter.get_transaction_history(sheet_id, 'A2:R100')
sqlite.insert_transaction_histories(records)
