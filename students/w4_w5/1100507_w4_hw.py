
# pip install requests beautifulsoup4

import time
import random
import requests
from bs4 import BeautifulSoup


class YahooStock:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

    def fetch_stock_info(self, stock_name):
        url = f'https://finance.yahoo.com/quote/{stock_name}'

        # 發送 HTTP 請求
        response = requests.get(url)

        # 使用 BeautifulSoup 解析 HTML
        self.stock_soup = BeautifulSoup(response.text, 'html.parser')

    def get_info(self):
        price_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})
        price_span = price_div.find('span').text

        price_change_element = price_div.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        price_change = price_change_element.find('span').text

        description = self.stock_soup.find('h1', {'class': 'yf-xxbei9'}).text
        
        return [price_span, price_change, description]


if __name__ == "__main__":
    yahoo_stock_src = YahooStock()
    stocks = ['AAPL', 'GOOGL', 'AMZN', 'INTC', 'AMD', 'NVDA', 'TSLA']

    print("Symbol\tStock Price\tChange\tDescription")
    
    for stock in stocks:
        print(stock, end='\t')
        yahoo_stock_src.fetch_stock_info(stock)
        info = yahoo_stock_src.get_info()
        
        for item in info:
            print(item, end='\t')

        print()