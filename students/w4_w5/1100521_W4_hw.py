#pip install requests beautifulsoup4

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
        

    def GetStockPrice(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})
        price_span = price_div.find('span').text
        return price_span
    
    def GetStockChange(self):
        change_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})
        change_finstreamer = change_div.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        change_span = change_finstreamer.find('span').text
        return change_span
    
    def GetStockDescription(self):
        Description_div = self.stock_soup.find('div', {'class': 'left yf-1s1umie wrap'})
        Description_span = Description_div.find('h1').text
        return Description_span
    

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    search_stocks = ['AAPL', 'GOOGL', 'AMZN','INTC','AMD','NVDA','TSLA']
    #print("NVDA Price")
    print("Symbol\tStock Price\tChange\tDescription")
    for i in search_stocks:
        print(i+' ', end='\t')
        yahoo_stock_src.FetchStockInfo(i)
        print(yahoo_stock_src.GetStockPrice(),end='\t\t')
        print(yahoo_stock_src.GetStockChange(),end='\t')
        print(yahoo_stock_src.GetStockDescription(),end='\n')