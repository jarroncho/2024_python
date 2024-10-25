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

        start_time = time.time()
        self.browser.get("https://finance.yahoo.com/quote/")
        print("加載頁面時間: ", time.time() - start_time)

    def __del__(self):
        self.browser.quit()

    def FetchStockInfo(self, stock_name):
        # 每次查詢前重新定位搜尋框和搜尋按鈕
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

        self.input.clear()  # 清空輸入框，避免輸入重複
        self.input.send_keys(stock_name)

        # 等待搜尋按鈕可點擊
        WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable(self.search)
        )

        self.search.click()
        start_time = time.time()
        # 等待搜尋按鈕消失或不再出現在DOM中
        WebDriverWait(self.browser, 30).until(
            EC.staleness_of(self.search)  # 等待按鈕變為無效
        )
        print("獲取股票 " + stock_name + " 頁面 ", time.time() - start_time)

        # 用BeautifulSoup解析HTML
        self.stock_soup = BeautifulSoup(self.browser.page_source, "lxml")

    def GetStockPrice(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})
        price_span = price_div.find('span').text
        return price_span
    
    def GetStockChange(self):
        change_div = self.stock_soup.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        change_span = change_div.find('span').text
        return change_span

    def GetStockDescription(self):
        Description_div = self.stock_soup.find('div', {'class': 'left yf-1s1umie wrap'})
        Description_span = Description_div.find('h1', {'class':'yf-xxbei9'}).text
        return Description_span

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    # 股票代號列表
    stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'INTC','AMD','NVDA','TSLA']  # 你可以在這裡加上其他股票代號

    result = []

    # 迭代處理每一支股票
    for stock_symbol in stock_symbols:
        yahoo_stock_src.FetchStockInfo(stock_symbol)
        price = yahoo_stock_src.GetStockPrice()
        change = yahoo_stock_src.GetStockChange()
        description = yahoo_stock_src.GetStockDescription()
        result.append((stock_symbol, price, change, description))

    # 保存到 Excel 檔案
    df = pd.DataFrame(result, columns=["Symbol", "Price", "Change", "Discription"])
    df.to_excel("stock_search.xlsx", sheet_name="stock", index=False)

