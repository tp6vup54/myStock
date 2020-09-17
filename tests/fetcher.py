from bs4 import BeautifulSoup
import unittest

from fetcher.id import StockIdFetcher


class TestFetcher(unittest.TestCase):
    def setUp(self):
        self.test_raw_text = """
    <body>
       <h2><strong><font class="h1">本國上市證券國際證券辨識號碼一覽表</font></strong></h2>
       <h2>
          <strong>
             <font class="h1">
                <center>最近更新日期:2020/08/28  </center>
             </font>
          </strong>
       </h2>
       <h2>
          <font color="red">
             <center>掛牌日以正式公告為準</center>
          </font>
       </h2>
       <table align="center"></table>
       <table class="h4" width="750" cellspacing="3" cellpadding="2" border="0" align="center">
          <tbody>
             <tr align="center">
                <td bgcolor="#D5FFD5">有價證券代號及名稱 </td>
                <td bgcolor="#D5FFD5">國際證券辨識號碼(ISIN Code)</td>
                <td bgcolor="#D5FFD5">上市日</td>
                <td bgcolor="#D5FFD5">市場別</td>
                <td bgcolor="#D5FFD5">產業別</td>
                <td bgcolor="#D5FFD5">CFICode</td>
                <td bgcolor="#D5FFD5">備註</td>
             </tr>
             <tr>
                <td colspan="7" bgcolor="#FAFAD2"><b> 股票 <b> </b></b></td>
             </tr>
             <tr>
                <td bgcolor="#FAFAD2">1101　台泥</td>
                <td bgcolor="#FAFAD2">TW0001101004</td>
                <td bgcolor="#FAFAD2">1962/02/09</td>
                <td bgcolor="#FAFAD2">上市</td>
                <td bgcolor="#FAFAD2">水泥工業</td>
                <td bgcolor="#FAFAD2">ESVUFR</td>
                <td bgcolor="#FAFAD2"></td>
             </tr>
             <tr>
                <td bgcolor="#FAFAD2">1102　亞泥</td>
                <td bgcolor="#FAFAD2">TW0001102002</td>
                <td bgcolor="#FAFAD2">1962/06/08</td>
                <td bgcolor="#FAFAD2">上市</td>
                <td bgcolor="#FAFAD2">水泥工業</td>
                <td bgcolor="#FAFAD2">ESVUFR</td>
                <td bgcolor="#FAFAD2"></td>
             </tr>
             <tr>
                <td colspan="7" bgcolor="#FAFAD2"><b> ETF <b> </b></b></td>
             </tr>
             <tr>
                <td bgcolor="#FAFAD2">0050　元大台灣50</td>
                <td bgcolor="#FAFAD2">TW0000050004</td>
                <td bgcolor="#FAFAD2">2003/06/30</td>
                <td bgcolor="#FAFAD2">上市</td>
                <td bgcolor="#FAFAD2"></td>
                <td bgcolor="#FAFAD2">CEOGEU</td>
                <td bgcolor="#FAFAD2"></td>
             </tr>
             <tr>
                <td bgcolor="#FAFAD2">0051　元大中型100</td>
                <td bgcolor="#FAFAD2">TW0000051002</td>
                <td bgcolor="#FAFAD2">2006/08/31</td>
                <td bgcolor="#FAFAD2">上市</td>
                <td bgcolor="#FAFAD2"></td>
                <td bgcolor="#FAFAD2">CEOGEU</td>
                <td bgcolor="#FAFAD2"></td>
             </tr>
             <tr>
                <td bgcolor="#FAFAD2">0052　富邦科技</td>
                <td bgcolor="#FAFAD2">TW0000052000</td>
                <td bgcolor="#FAFAD2">2006/09/12</td>
                <td bgcolor="#FAFAD2">上市</td>
                <td bgcolor="#FAFAD2"></td>
                <td bgcolor="#FAFAD2">CEOGEU</td>
                <td bgcolor="#FAFAD2"></td>
             </tr>
             <td bgcolor="#FAFAD2"></td>
             </tr>
          </tbody>
       </table>
       <font color="red">
          <center>掛牌日以正式公告為準</center>
       </font>
    </body>
            """

    def test_get_stock_id(self):
        fetcher = StockIdFetcher()
        fetcher.soup = BeautifulSoup(self.test_raw_text, 'html.parser')
        result = fetcher.get_stock_ids()
        self.assertEqual('1101', result[0])
        self.assertEqual('1102', result[-1])
        self.assertEqual(2, len(result))

    def test_get_etf_id(self):
        fetcher = StockIdFetcher()
        fetcher.soup = BeautifulSoup(self.test_raw_text, 'html.parser')
        result = fetcher.get_etf_ids()
        self.assertEqual('0050', result[0])
        self.assertEqual('0052', result[-1])
        self.assertEqual(3, len(result))


if __name__ == '__main__':
    unittest.main()
