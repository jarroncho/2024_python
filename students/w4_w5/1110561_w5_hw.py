from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

class YahooStock():
    def __init__(self):# 安裝Chrome驅動程式及建立Chrome物件
        self.browser = webdriver.Chrome()
        self.browser.get("https://finance.yahoo.com/quote/")

        locator = (By.ID, "ybar-sbq")  #定位器
        self.input = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(locator))
        locator = (By.ID, "ybar-search") #定位器
        self.search = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located(locator))
    
    def __del__(self):
        self.browser.quit()

    def FetchStockInfo(self,stock_name):
        locator = (By.ID, "ybar-sbq") #重新定位
        self.input = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located(locator))
        locator = (By.ID, "ybar-search") #重新定位
        self.search = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located(locator))
        self.input.send_keys(stock_name)

        WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(self.search))# Wait for the search button to be clickable
        self.search.click()

        WebDriverWait(self.browser, 30).until(EC.staleness_of(self.search))  # Wait for the button to go stale
        self.stock_soup = BeautifulSoup(self.browser.page_source, "lxml")# 用BeautifulSoup解析HTML
        
    def GetStockPrice(self):
        price_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_span = price_div.find('span').text
        return price_span
    
    def GetStockChange(self):
        change_div = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})# 尋找包含變化百分比的 fin-streamer 元素
        change_span = change_div.find('span').text.replace('(', '').replace(')', '').replace('%', '').strip()
        return change_span
    
    def GetStockDes(self):
        des_div = self.stock_soup.find('div', {'class':'left yf-1s1umie wrap'})
        des_h1 = des_div.find('h1', {'class':'yf-xxbei9'}).text
        return des_h1

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()
    company = ['AAPL', 'GOOGL', 'AMZN', 'INTC', 'AMD', 'NVDA', 'TSLA']
    result = []
    
    for stock_symbol in company:
        yahoo_stock_src.FetchStockInfo(stock_symbol)
        price = yahoo_stock_src.GetStockPrice()
        change = yahoo_stock_src.GetStockChange()
        description = yahoo_stock_src.GetStockDes()
        result.append((stock_symbol,price, change, description))

    df = pd.DataFrame(result, columns=["Symbol", "Stock Price", "Change", "Description"])
    df.to_excel("stock_search.xlsx", sheet_name="stock", index=False)