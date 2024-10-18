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
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        change_div = self.stock_soup.find('fin-streamer',{'class':'priceChange yf-1tejb6'})
        change_span = change_div.find('span').text
        return change_span
    def GetStockDescription(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        Description_div = self.stock_soup.find('section',{'class':'yf-xxbei9'})
        Description_span = Description_div.find('span').text
        return Description_span

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    print("Symbol\tStock Price\tChange\tDescription")
    yahoo_stock_src.FetchStockInfo('AAPL')
    print("AAPL\t",yahoo_stock_src.GetStockPrice(),"\t",yahoo_stock_src.GetStockChange(),"\t","Apple Inc. (AAPL)")
    yahoo_stock_src.FetchStockInfo('GOOGL')
    print("GOOGL\t",yahoo_stock_src.GetStockPrice(),"\t",yahoo_stock_src.GetStockChange(),"\t","Alphabet Inc(GOOGL)")
    yahoo_stock_src.FetchStockInfo('AMZN')
    print("AMZN\t",yahoo_stock_src.GetStockPrice(),"\t",yahoo_stock_src.GetStockChange(),"\t","Amazon.com, Inc. (AMZN)")
    yahoo_stock_src.FetchStockInfo('INTC')
    print("INTC\t",yahoo_stock_src.GetStockPrice(),"\t\t",yahoo_stock_src.GetStockChange(),"\t","Intel Corporation (INTC)")
    yahoo_stock_src.FetchStockInfo('AMD')
    print("AMD\t",yahoo_stock_src.GetStockPrice(),"\t",yahoo_stock_src.GetStockChange(),"\t","Advanced Micro Devices, Inc. (AMD)")
    yahoo_stock_src.FetchStockInfo('NVDA')
    print("NVDA\t",yahoo_stock_src.GetStockPrice(),"\t",yahoo_stock_src.GetStockChange(),"\t","NVIDIA Corporation (NVDA)")
    yahoo_stock_src.FetchStockInfo('TSLA')
    print("TSLA\t",yahoo_stock_src.GetStockPrice(),"\t",yahoo_stock_src.GetStockChange(),"\t","Tesla, Inc. (TSLA)")