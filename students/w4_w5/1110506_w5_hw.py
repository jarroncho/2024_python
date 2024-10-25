import time
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd

class YahooStock():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

    def FetchStockInfo(self, stock_name):
        url = 'https://finance.yahoo.com/quote/' + stock_name
        response = requests.get(url, headers=self.headers)

        # 用BeautifulSoup解析HTML
        self.stock_soup = BeautifulSoup(response.text, 'html.parser')

    def GetStockDescription(self):
        try:
            description = self.stock_soup.find('h1').text
            return description
        except AttributeError:
            return "N/A"

    def GetStockPrice(self):
        try:
            price_span = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
            return price_span
        except AttributeError:
            return "N/A"

    def GetStockChange(self):
        try:
            change_span = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'}).text
            return change_span
        except (AttributeError, IndexError):
            return "N/A"


if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    search_stocks = ['AAPL', 'GOOGL', 'AMZN', 'INTC', 'AMD', 'NVDA', 'TSLA']
    
    # 儲存結果的列表
    stock_data = []

    for stock in search_stocks:
        yahoo_stock_src.FetchStockInfo(stock)
        stock_price = yahoo_stock_src.GetStockPrice()
        stock_change = yahoo_stock_src.GetStockChange()
        stock_description = yahoo_stock_src.GetStockDescription()
        
        # 將結果追加到 stock_data 列表
        stock_data.append([stock, stock_price, stock_change, stock_description])
        
        # 隨機等待 1 到 3 秒以避免被封鎖
        time.sleep(random.randint(1, 3))
    
    # 創建DataFrame
    df = pd.DataFrame(stock_data, columns=['Symbol', 'Stock Price', 'Change', 'Description'])
    
    # 儲存到 Excel
    df.to_excel('stock_data.xlsx', index=False)

    print("資料已成功儲存到 'stock_data.xlsx'")
