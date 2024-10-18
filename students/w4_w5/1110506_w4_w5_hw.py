import requests
from bs4 import BeautifulSoup

class YahooStock():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

    def FetchStockInfo(self, stock_name):
        url = f'https://finance.yahoo.com/quote/{stock_name}'
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                self.stock_soup = BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Failed to retrieve data for {stock_name}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching stock info: {e}")

    def GetStockPrice(self):
        try:
            price_span = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
            return price_span
        except Exception as e:
            return f"Error retrieving price: {e}"

    def GetStockChange(self):
        try:
            change_span = self.stock_soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'}).text
            return change_span
        except Exception as e:
            return f"Error retrieving change: {e}"

    def GetCompanyName(self):
        try:
            # Extract the company name from the title tag, which contains the company name followed by stock symbol
            company_name = self.stock_soup.find('title').text.split(" stock")[0]  # Extract before 'stock' keyword in title
            return company_name
        except Exception as e:
            return f"Error retrieving company name: {e}"

if __name__ == "__main__":
    yahoo_stock_src = YahooStock()

    search_stocks = ['AAPL', 'GOOGL', 'AMZN', 'INTC', 'AMD', 'NVDA', 'TSLA']
    print(f"{'Symbol':<6}\t{'Stock Price':<12}\t{'Change':<8}\t{'Company Name':<30}")

    for stock in search_stocks:
        yahoo_stock_src.FetchStockInfo(stock)
        stock_price = yahoo_stock_src.GetStockPrice()
        stock_change = yahoo_stock_src.GetStockChange()
        company_name = yahoo_stock_src.GetCompanyName()
        
        print(f"{stock:<6}\t{stock_price:<12}\t{stock_change:<8}\t{company_name:<30}")
