import time
import random
import requests
from bs4 import BeautifulSoup


class YahooStock:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

    def fetch_stock_info(self, stock_name):
        url = f'https://finance.yahoo.com/quote/{stock_name}'
        try:
            # 發送HTTP請求
            response = requests.get(url, headers=self.headers)
            # 用BeautifulSoup解析HTML
            self.stock_soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching data for {stock_name}: {e}")
            self.stock_soup = None

    def get_stock_price(self):
        try:
            price_div = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})
            stock_price = price_div.find('span').text
            return stock_price
        except AttributeError:
            return 'N/A'

    def get_stock_change(self):
        try:
            change_div = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})
            stock_change = change_div.find_all('span')[1].text
            return stock_change
        except (AttributeError, IndexError):
            return 'N/A'

    def get_stock_description(self):
        try:
            description_div = self.stock_soup.find('section', {'class': 'quote-sub-section Mt(30px)'})
            description_span = description_div.find('span').text
            return description_span
        except AttributeError:
            return 'No description available'


if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    stocks = {
        'AAPL': 'Apple Inc. (AAPL)',
        'GOOGL': 'Alphabet Inc. (GOOGL)',
        'AMZN': 'Amazon.com, Inc. (AMZN)',
        'INTC': 'Intel Corporation (INTC)',
        'AMD': 'Advanced Micro Devices, Inc. (AMD)',
        'NVDA': 'NVIDIA Corporation (NVDA)',
        'TSLA': 'Tesla, Inc. (TSLA)'
    }

    print("Symbol\tStock Price\tChange\tDescription")

    for stock_symbol, stock_description in stocks.items():
        yahoo_stock_src.fetch_stock_info(stock_symbol)
        print(f"{stock_symbol}\t{yahoo_stock_src.get_stock_price()}\t{yahoo_stock_src.get_stock_change()}\t{stock_description}")
