import time
import requests
import pandas as pd
from io import StringIO
import yfinance as yf
from pathlib import Path

url_map = {
    'nifty50': 'https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv',
    'nifty100': 'https://nsearchives.nseindia.com/content/indices/ind_nifty100list.csv',
    'nifty200': 'https://nsearchives.nseindia.com/content/indices/ind_nifty200list.csv',
    'nifty500': 'https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv',
    'niftymidcap150': 'https://nsearchives.nseindia.com/content/indices/ind_niftymidcap150list.csv',
    'niftysmallcap250': 'https://nsearchives.nseindia.com/content/indices/ind_niftysmallcap250list.csv'
}

class DataFetcher:
    
    def get_stock_ticker(self, index_name) -> pd.DataFrame:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try: 
            print(f'Downloading the stocks list for index {index_name}')
            response = requests.get(url_map[index_name], headers=headers)
            print(f'Downloaded the stocks list for index {index_name}')
            return pd.read_csv(StringIO(response.text))
        except Exception as e:
            print(f'Error in downloading stock list {e.with_traceback}')
            raise IOError("Error in getting ticker names", e)
        
        
    def extract_symbol(self, df):
        return [self.modify_ticker(symbol) for symbol in df['Symbol'].tolist()]

    def modify_ticker (self, symbol):
        return symbol + '.NS'

            
    def get_comprehensive_stock_data(self, symbol):
        """Get price data + all fundamental data for a stock"""
    
        print(f"Fetching data for {symbol}...")
        ticker = yf.Ticker(symbol)
        
        try:
            # 1. Price Data
            price_data = ticker.history(start='2022-04-01', end='2025-12-30')
            
            # 2. Current Fundamentals
            info = ticker.info
            current_fundamentals = {
                'Date': pd.Timestamp.now(),
                'Symbol': symbol,
                # 'PE_Ratio': info.get('trailingPE'),
                # 'Forward_PE': info.get('forwardPE'),
                # 'PB_Ratio': info.get('priceToBook'),
                # 'PS_Ratio': info.get('priceToSalesTrailing12Months'),
                # 'PEG_Ratio': info.get('pegRatio'),
                'EPS': info.get('trailingEps'),
                'Forward_EPS': info.get('forwardEps'),
                'Dividend_Yield': info.get('dividendYield'),
                # 'Market_Cap': info.get('marketCap'),
                # 'Enterprise_Value': info.get('enterpriseValue'),
                'Book_Value_Per_Share': info.get('bookValue'),
                # 'Price_to_Book': info.get('priceToBook'),
                'ROE': info.get('returnOnEquity'),
                'ROA': info.get('returnOnAssets'),
                'ROIC': info.get('returnOnCapital'),
                'Profit_Margin': info.get('profitMargins'),
                'Operating_Margin': info.get('operatingMargins'),
                'Gross_Margin': info.get('grossMargins'),
                'Revenue_Per_Share': info.get('revenuePerShare'),
                'Debt_to_Equity': info.get('debtToEquity'),
                'Current_Ratio': info.get('currentRatio'),
                'Quick_Ratio': info.get('quickRatio'),
                'Revenue_Growth': info.get('revenueGrowth'),
                'Earnings_Growth': info.get('earningsGrowth'),
                'Operating_Cashflow': info.get('operatingCashflow'),
                'Free_Cashflow': info.get('freeCashflow'),
                'Beta': info.get('beta'),
                'Current_Price': info.get('currentPrice'),
            }
            
            # 3. Financial Statements
            income_stmt = ticker.financials
            balance_sheet = ticker.balance_sheet
            cashflow = ticker.cashflow
            
            # 4. Quarterly data for more granular analysis
            quarterly_financials = ticker.quarterly_financials
            
            return {
                'price_data': price_data,
                'current_fundamentals': current_fundamentals,
                'income_statement': income_stmt,
                'balance_sheet': balance_sheet,
                'cashflow': cashflow,
                'quarterly_financials': quarterly_financials
            }
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
            
    def save_csv(self, data, symbol, path):
        if data:
            """
                currently we are only saving fundamental data
                once the model is working then we will start using other params as well
            """
            print (f'Saving details for {symbol}')
            target_file = path + '/data/raw/' + symbol
            # Save price data
            # data['price_data'].to_csv(target_file + '_prices.csv')
            
            # Save current fundamentals
            pd.DataFrame([data['current_fundamentals']]).to_csv(target_file + '_fundamentals.csv', index=False)
            
            # Save financial statements
            # data['income_statement'].to_csv(target_file + '_income_stmt.csv')
            # data['balance_sheet'].to_csv(target_file + '_balance_sheet.csv')
            # data['cashflow'].to_csv(target_file + '_cashflow.csv')
            # data['quarterly_financials'].to_csv(target_file + '_quarterly.csv')

    def fetch_all_data(self, path):
        data_fetcher = DataFetcher()
        print('Downloading stock list')
        df = data_fetcher.get_stock_ticker('nifty500')
        all_symbols = data_fetcher.extract_symbol(df)
        for s in all_symbols:
            print(f'Downloading stock data for {s}')
            data = data_fetcher.get_comprehensive_stock_data(s)
            data_fetcher.save_csv(data, s, path)
            time.sleep(1)
            