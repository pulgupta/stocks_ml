import time
import requests
import pandas as pd
from io import StringIO
import yfinance as yf

url_map = {
    'nifty50': 'https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv',
    'nifty100': 'https://nsearchives.nseindia.com/content/indices/ind_nifty100list.csv',
    'nifty200': 'https://nsearchives.nseindia.com/content/indices/ind_nifty200list.csv',
    'nifty500': 'https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv',
    'niftymidcap150': 'https://nsearchives.nseindia.com/content/indices/ind_niftymidcap150list.csv',
    'niftysmallcap250': 'https://nsearchives.nseindia.com/content/indices/ind_niftysmallcap250list.csv'
}

class DataManager:
    
    def get_stock_ticker(self, index_name): 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try: 
            print(f'Downloading the stocks list for index {index_name}')
            response = requests.get (url_map[index_name], headers=headers)
            print(f'Downloaded the stocks list for index {index_name}')
            return pd.read_csv(StringIO(response.text))
        except Exception as e:
            print(f'Error in downloading stock list {e.with_traceback}')
            raise IOError("Error in getting ticker names", e)
        
        
    def extract_symbol(self, df):
        return [symbol + '.NS' for symbol in df['Symbol'].tolist()]
    
    def save_stock_details(self, symbols):
        total_symbols = len(symbols)
        print(f'total symbols are {total_symbols}')
        for symbol in symbols: 
            print (f'Downloading data for {symbol}')
            dat = yf.download(symbol, period='1mo')
            dat.to_csv('/Users/pulgupta/Documents/codes/Stocks-ML/data/raw/' + symbol + '.csv'),
            time.sleep(10)
            

data_manager = DataManager()
data_manager.save_stock_details(data_manager.extract_symbol(data_manager.get_stock_ticker('nifty50')))

            