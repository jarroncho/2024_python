# pip install requests beautifulsoup4

import time
import random
import requests
from bs4 import BeautifulSoup


class YahooStock():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

    def FetchStockInfo(self, sotck_name):
        url = 'https://finance.yahoo.com/quote/' + sotck_name

        # 發送HTTP請求
        response = requests.get(url)

        # 用BeautifulSoup解析HTML
        self.stock_soup = BeautifulSoup(response.text, 'html.parser')

    def GetStockPrice(self):
        # stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})
        price_span = price_div.find('span').text
        return price_span
    def GetStockChange(self):
        price_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})
        change = price_div.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        change_span = change.find('span').text
        return change_span
    def GetStockDescription(self):
        description_span = self.stock_soup.find('h1', {'class': 'yf-xxbei9'}).text
        return description_span


if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    #Apple, Google, Amazon, Intel, AMD, NVDA, TESLA
    stocks = ['AAPL', 'GOOGL', 'AMZN', 'INTC', 'AMD', 'NVDA', 'TSLA']
    print('Symbol\tStock Price\tChange\tDescription')
    for stock in stocks:
        print(stock+' ', end='\t')
        yahoo_stock_src.FetchStockInfo(stock)
        print(yahoo_stock_src.GetStockPrice(), end='\t\t')
        yahoo_stock_src.FetchStockInfo(stock)
        print(yahoo_stock_src.GetStockChange(), end='\t')
        yahoo_stock_src.FetchStockInfo(stock)
        print(yahoo_stock_src.GetStockDescription(), end='\t')
        print()
