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
    def Change(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        change_div = self.stock_soup.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        change_span = change_div.find('span').text
        return change_span
    def Disc(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        disc_div = self.stock_soup.find('section', {'class': 'container yf-xxbei9 paddingRight'})
        disc_span = disc_div.find('h1', {'class': 'yf-xxbei9'}).text
        return disc_span



if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    print("{:<8} {:<8} {:<10} {}".format("Symbol", "Stock", "Change", "Description"))

    yahoo_stock_src.FetchStockInfo('AAPL')
    print("{:<8} {:<8} {:<10} {}".format("AAPL", yahoo_stock_src.GetStockPrice(), yahoo_stock_src.Change(), yahoo_stock_src.Disc()))

    yahoo_stock_src.FetchStockInfo('GOOGL')
    print("{:<8} {:<8} {:<10} {}".format("GOOGL", yahoo_stock_src.GetStockPrice(), yahoo_stock_src.Change(), yahoo_stock_src.Disc()))

    yahoo_stock_src.FetchStockInfo('AMZN')
    print("{:<8} {:<8} {:<10} {}".format("AMZN", yahoo_stock_src.GetStockPrice(), yahoo_stock_src.Change(), yahoo_stock_src.Disc()))

    yahoo_stock_src.FetchStockInfo('INTC')
    print("{:<8} {:<8} {:<10} {}".format("INTC", yahoo_stock_src.GetStockPrice(), yahoo_stock_src.Change(), yahoo_stock_src.Disc()))

    yahoo_stock_src.FetchStockInfo('AMD')
    print("{:<8} {:<8} {:<10} {}".format("AMD", yahoo_stock_src.GetStockPrice(), yahoo_stock_src.Change(), yahoo_stock_src.Disc()))

    yahoo_stock_src.FetchStockInfo('NVDA')
    print("{:<8} {:<8} {:<10} {}".format("NVDA", yahoo_stock_src.GetStockPrice(), yahoo_stock_src.Change(), yahoo_stock_src.Disc()))

    yahoo_stock_src.FetchStockInfo('TLSA')
    print("{:<8} {:<8} {:<10} {}".format("TLSA", yahoo_stock_src.GetStockPrice(), yahoo_stock_src.Change(), yahoo_stock_src.Disc()))
    
   
    