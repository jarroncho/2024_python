from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

class YahooStock:
    def __init__(self):
        # 初始化Chrome物件
        self.browser = webdriver.Chrome()

    def __del__(self):
        self.browser.quit()

    def fetch_stock_info(self, stock_name):
        # 進入Yahoo股票頁面並搜索股票
        self.browser.get("https://finance.yahoo.com/quote/")
        
        # 定位搜尋輸入框和搜尋按鈕
        input_box = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.ID, "ybar-sbq"))
        )
        search_button = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.ID, "ybar-search"))
        )

        input_box.clear()
        input_box.send_keys(stock_name)
        
        # 點擊搜尋按鈕
        WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(search_button)).click()

        # 等待搜尋完成並抓取資料
        WebDriverWait(self.browser, 30).until(EC.staleness_of(search_button))
        self.stock_soup = BeautifulSoup(self.browser.page_source, "lxml")

    def get_stock_price(self):
        # 獲取股票價格
        price_span = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
        return price_span

    def get_stock_change(self):
        # 獲取股票變化
        change_span = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'}).text
        return change_span

    def get_stock_description(self):
        # 獲取股票描述
        description_span = self.stock_soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text
        return description_span

if __name__ == "__main__":
    yahoo_stock = YahooStock()
    
    stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'INTC', 'AMD', 'NVDA', 'TSLA']
    result = []

    for symbol in stock_symbols:
        yahoo_stock.fetch_stock_info(symbol)
        price = yahoo_stock.get_stock_price()
        change = yahoo_stock.get_stock_change()
        description = yahoo_stock.get_stock_description()
        
        # 加入結果列表
        result.append((symbol, price, change, description))

    # 保存到Excel檔案
    df = pd.DataFrame(result, columns=["Symbol", "Stock Price", "Change", "Description"])
    df.to_excel("stock_search.xlsx", sheet_name="stock", index=False)
