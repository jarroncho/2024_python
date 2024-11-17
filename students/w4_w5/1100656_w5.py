from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


class YahooStock():
    def __init__(self):
        self.browser = webdriver.Chrome()
        start_time = time.time()
        self.browser.get("https://finance.yahoo.com/quote/")
        print("加載頁面時間: ", time.time() - start_time)

    def __del__(self):
        self.browser.quit()

    def FetchStockInfo(self, stock_name):
        locator = (By.ID, "ybar-sbq")
        self.input = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(locator),
            "等待搜尋輸入框超時"
        )

        locator = (By.ID, "ybar-search")
        self.search = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(locator),
            "等待搜尋按鈕超時"
        )

        self.input.clear() 
        self.input.send_keys(stock_name)
        WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable(self.search)
        )

        self.search.click()
        start_time = time.time()
        WebDriverWait(self.browser, 30).until(
            EC.staleness_of(self.search)  
        )
        self.stock_soup = BeautifulSoup(self.browser.page_source, "lxml")

    def GetStockPrice(self):
        price_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})
        price_span = price_div.find('span').text
        return price_span
    
    def GetStockChange(self):
        change_div = self.stock_soup.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        change_span = change_div.find('span').text
        return change_span

    def GetStockDescription(self):
        Description_span = self.stock_soup.find('h1', {'class': 'yf-xxbei9'}).text
        return Description_span

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()
    stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'INTC','AMD','NVDA','TSLA'] 
    result = []
    print('Symbol  Stock Price   Change  Description')
    flag=0
    for stock_symbol in stock_symbols:
        yahoo_stock_src.FetchStockInfo(stock_symbol)
        price = yahoo_stock_src.GetStockPrice()
        change = yahoo_stock_src.GetStockChange()
        description = yahoo_stock_src.GetStockDescription()
        result.append((stock_symbol, price, change, description))
        print(result[flag])
        flag+=1
    df = pd.DataFrame(result, columns=["Symbol", "Price", "Change", "Discription"])
    df.to_excel("stock_search.xlsx", sheet_name="stock", index=False)