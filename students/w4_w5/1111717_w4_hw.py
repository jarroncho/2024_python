import requests
from bs4 import BeautifulSoup
flag=0

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

    def GetStockPrice(self):
        global flag  
        try:
            price_div = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            if price_div:
                difference=self.Getdifference()
                print(f"{stock_name[flag]}\t{price_div.text}\t{difference}\t{self.GetDescription()}") 
                flag+=1
                return price_div.text
            else:
                print("Could not find stock price in the response.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    def Getdifference(self):
        difference_fin=self.stock_soup.find('fin-streamer', {'class': 'priceChange yf-1tejb6'})
        difference_span=difference_fin.find('span').text
        return difference_span
    def GetDescription(self):
        description_section=self.stock_soup.find('section', {'class': 'container yf-xxbei9 paddingRight'})
        description_h1=description_section.find('h1', {'class': 'yf-xxbei9'}).text
        return description_h1

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()
    print('Symbol\tStock Price\tChange\tDescription')
    stock_name = ['AAPL','GOOGL','AMZN','INTC','AMD','NVDA','TSLA']
    for i in range(0,len(stock_name)):
        yahoo_stock_src.FetchStockInfo(stock_name[i])
        price = yahoo_stock_src.GetStockPrice()
