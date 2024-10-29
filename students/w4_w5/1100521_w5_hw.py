from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


class YahooStock():
    def __init__(self):
        # 安裝Chrome驅動程式及建立Chrome物件
        self.browser = webdriver.Chrome()

        #開啟頁面
        start_time=time.time()
        self.browser.get("https://finance.yahoo.com/quote/")
        print("load page time: ",time.time()-start_time)
        #定位搜索框
        locator = (By.ID, "ybar-sbq")  # 定位器
        start_time=time.time()
        self.input = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(locator),
            "Timeout while waiting for search input box")
        print("get input time:",time.time()-start_time)
        #定位搜索鍵
        locator = (By.ID, "ybar-search")
        start_time=time.time()
        self.search = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(locator),
            "Timeout while waiting for search button")
        print("get search time",time.time()-start_time)
    
    def __del__(self):
        self.browser.quit()
    
    def Refetch(self):  #重新定位
        start_time=time.time()
        self.browser.get("https://finance.yahoo.com/quote/")
        print("load page time: ",time.time()-start_time)
        locator = (By.ID, "ybar-sbq")  # 定位器
        start_time=time.time()
        self.input = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(locator),
            "Timeout while waiting for search input box")
        print("get input time:",time.time()-start_time)

        locator = (By.ID, "ybar-search")
        start_time=time.time()
        self.search = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(locator),
            "Timeout while waiting for search button")
        print("get search time",time.time()-start_time)

    def FetchStockInfo(self,stock_name):
        
        self.input.send_keys(stock_name)

        # Wait for the search button to be clickable
        WebDriverWait(self.browser, 30).until(
        EC.element_to_be_clickable(self.search)
        )
        
        self.search.click()
        start_time=time.time()
         # Wait until the search button is no longer visible or present in the DOM
        WebDriverWait(self.browser, 30).until(
        EC.staleness_of(self.search)  # Wait for the button to go stale
        )
        print("get stock "+stock_name+" page ",time.time()-start_time)

        # 用BeautifulSoup解析HTML
        self.stock_soup = BeautifulSoup(self.browser.page_source, "lxml")
        
        
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
    
    #stock_symbol='NVDA'
    search_stocks = ['AAPL', 'GOOGL', 'AMZN','INTC','AMD','NVDA','TSLA']
    result = []
    for stock in search_stocks:
        yahoo_stock_src.Refetch()
        yahoo_stock_src.FetchStockInfo(stock)
        price = yahoo_stock_src.GetStockPrice()
        change=yahoo_stock_src.GetStockChange()
        description=yahoo_stock_src.GetStockDescription()
        result.append((stock,price,change,description))

    #save to excel file
    df = pd.DataFrame(result, columns=["Symbol", "Stock Price","Change","Description"])
    df.to_excel("stock_search.xlsx", sheet_name="stock", index=False)