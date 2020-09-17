from bs4 import BeautifulSoup
import requests


class StockIdFetcher:
    def __init__(self):
        self.soup = None
        self.TWSE_IDS_URL = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'

    def get_stock_ids(self) -> list:
        return self._get_ids_with_title('股票')

    def get_etf_ids(self) -> list:
        return self._get_ids_with_title('ETF')

    def _get_ids_with_title(self, title: str) -> list:
        if not self.soup:
            raw_text = requests.get(self.TWSE_IDS_URL).text
            self.soup = BeautifulSoup(raw_text, 'html.parser')
        trs = self.soup.find_all('tr')
        ids = []
        is_started = False
        for tr in trs:
            texts = tr.text.split()
            if len(texts) == 1:
                if title in texts:
                    is_started = True
                    continue
                elif is_started:
                    break
            if is_started:
                ids.append(texts[0])
        return ids
