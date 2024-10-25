#pip install gspread oauth2client

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
        
        
    def GetStockDescription(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_div = self.stock_soup.find('div', {'class': 'left yf-1s1umie wrap'})
        price_span = price_div.find('h1').text
        return price_span
    
    def GetStockPrice(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_div = self.stock_soup.find('div', {'class': 'price yf-1s1umie'})
        price_span = price_div.find('span').text
        return price_span
    
    def GetStockChange(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_div = self.stock_soup.find('div', {'class': 'price yf-1s1umie'})
        price_span = price_div.find('span',{'class': 'change'}).text
        return price_span
    
    


if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    search_stocks = ['AAPL', 'GOOGL', 'AMZN','INTC','AMD','NVDA','TSLA']  
    #search_stocks = ['NVDA']  
    print("Symbol\tStock Price\tChange\tDescription")
    for stock in search_stocks:
        yahoo_stock_src.FetchStockInfo(stock)
        print(
                stock+"\t"+                
                yahoo_stock_src.GetStockPrice()+"\t\t"+
                yahoo_stock_src.GetStockChange()+"\t"+
                yahoo_stock_src.GetStockDescription()+"\t")
                
              
            
        
        
  
