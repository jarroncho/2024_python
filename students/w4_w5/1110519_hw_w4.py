import requests
from bs4 import BeautifulSoup

class YahooStock():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

    def fetch_stock_info(self, stock_name):
        url = 'https://finance.yahoo.com/quote/' + stock_name 
        response = requests.get(url, headers=self.headers)
        self.stock_soup = BeautifulSoup(response.text, 'html.parser')

    def get_stock_price(self):
        try:
            price_span = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
            return price_span
        except AttributeError:
            return "N/A"

    def get_stock_change(self):
        try:
            change_span = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketChange'}).text
            return change_span
        except AttributeError:
            return "N/A"

    def get_stock_description(self):
        try:
            # 嘗試從不同位置抓取公司名稱
            description = self.stock_soup.find('div', {'class': 'D(ib) Mt(-5px) Maw(60%) Ov(h)'}).find('h1').text
            return description
        except AttributeError:
            return "N/A"

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    # 搜尋的股票列表
    stock_list = ['AAPL', 'GOOGL', 'AMZN', 'INTC', 'AMD', 'NVDA', 'TSLA']

    # 打印表格標題
    print(f"{'Symbol':<6} {'Stock Price':<12} {'Change':<8} {'Description'}")
    print("-" * 60)

    # 獲取每隻股票的價格、變動值和描述
    for stock in stock_list:
        yahoo_stock_src.fetch_stock_info(stock)
        stock_price = yahoo_stock_src.get_stock_price()
        stock_change = yahoo_stock_src.get_stock_change()
        stock_description = yahoo_stock_src.get_stock_description()
        
        # 格式化輸出
        print(f"{stock:<6} {stock_price:<12} {stock_change:<8} {stock_description}")
