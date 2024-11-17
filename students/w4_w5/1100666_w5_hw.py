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
    
    def __del__(self):
        self.browser.quit()

    def FetchStockInfo(self, stock_name):
        # 重新定位输入框
        input_box = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.ID, "ybar-sbq"))
        )
        input_box.clear()  # 清除之前的输入
        input_box.send_keys(stock_name)

        # 重新定位搜索按钮并点击
        search_button = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.ID, "ybar-search"))
        )
        search_button.click()

        # 等待页面加载完成
        WebDriverWait(self.browser, 30).until(
            EC.staleness_of(search_button)  # 等待按钮失效
        )
        time.sleep(2)  # 简单延迟，确保页面完全加载

        # 用 BeautifulSoup 解析新的页面
        self.stock_soup = BeautifulSoup(self.browser.page_source, "lxml")

    def Getdifference(self):
        difference_fin=self.stock_soup.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        difference_span=difference_fin.find('span').text
        return difference_span
    def GetDescription(self):
        description_section=self.stock_soup.find('section', {'class': 'container yf-xxbei9 paddingRight'})
        description_h1=description_section.find('h1', {'class': 'yf-xxbei9'}).text
        return description_h1
    def GetStockPrice(self):
        #stock_price = self.stock_soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        price_div = self.stock_soup.find('div', {'class': 'container yf-1tejb6'})
        price_span = price_div.find('span').text
        return price_span
    
if __name__ == "__main__":
    yahoo_stock_src = YahooStock()
    stock_name = ['AAPL','GOOGL','AMZN','INTC','AMD','NVDA','TSLA']
    result=[]
    print('Symbol\tStock Price\tChange\tDescription')
    for i in range(len(stock_name)):
        yahoo_stock_src.FetchStockInfo(stock_name[i])
        price = yahoo_stock_src.GetStockPrice()
        change= yahoo_stock_src.Getdifference()
        disc  = yahoo_stock_src.GetDescription()
        print(stock_name[i],"\t",price,'\t',change,'t',disc)
        result.append((stock_name[i],price,change,disc))

    #save to excel file
    df = pd.DataFrame(result, columns=["Symbol", "Stock Price", "Change", "Description"])
    df.to_excel("stock_search.xlsx", sheet_name="stock", index=False)