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

    def FetchStockInfo(self,stock_name):
        url = 'https://finance.yahoo.com/quote/' + stock_name 

        # 發送HTTP請求
        response = requests.get(url)

        # 用BeautifulSoup解析HTML
        self.stock_soup = BeautifulSoup(response.text, 'html.parser')

    def Get_Price_Change_Description(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_div = self.stock_soup.find('div', {'class': 'container yf-aay0dk'})
        price_span = price_div.find('span').text

        priceChange = price_div.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        change = priceChange.find('span').text

        Description = self.stock_soup.find('h1', {'class': 'yf-xxbei9'}).text
        
        PCD = [price_span,change,Description]
        return PCD


if __name__ == "__main__":
    yahoo_stock_src = YahooStock()
    stock=['AAPL','GOOGL','AMZN','INTC','AMD','NVDA','TSLA']

    print("Symbol\tStock Price\tChange\tDescription")
    for a in stock:
        print(a,end='\t')
        yahoo_stock_src.FetchStockInfo(a)
        PCD = yahoo_stock_src.Get_Price_Change_Description()
        for i in range(len(PCD)):
            if i == 0:
                print(PCD[i], end='\t\t')
            else:
                print(PCD[i], end='\t')
        print()



   
