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

    def FetchStockInfo(self,sotck_name):
        
        
        url = 'https://finance.yahoo.com/quote/' + sotck_name 

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
        # 尋找包含變化百分比的 fin-streamer 元素
        change_div = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
        change_span = change_div.find('span').text.replace('(', '').replace(')', '').replace('%', '').strip()
        return change_span
    
    def GetStockDes(self):
        des_div = self.stock_soup.find('div', {'class':'left yf-1s1umie wrap'})
        des_h1 = des_div.find('h1', {'class':'yf-xxbei9'}).text
        return des_h1
        
print('Symbol\tStock Price\tChange\tDescription')
companylist = ['AAPL', 'GOOGL', 'AMZN', 'INTC', 'AMD', 'NVDA', 'TSLA']

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    for i in range(0, 7):
        yahoo_stock_src.FetchStockInfo(companylist[i])
       # print(companylist[i]+'\t'+yahoo_stock_src.GetStockPrice()+'\t'+yahoo_stock_src.GetStockChange())
        print(f'{companylist[i]}\t{yahoo_stock_src.GetStockPrice()}\t\t{yahoo_stock_src.GetStockChange()}\t{yahoo_stock_src.GetStockDes()}')