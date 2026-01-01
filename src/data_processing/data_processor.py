import os
import pandas as pd
from pathlib import Path

class DataProcessor:

    def load_data(self, path):
        csv_files = list(Path(path).glob("*.csv"))
        all_data = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            all_data.append(df)

        return pd.concat(all_data, ignore_index=True)

    def prepare_data(self, path):
        df:pd.DataFrame = self.load_data(path)
        df_cleaned = df.dropna(subset=['Current_Price'])
        Y = df_cleaned['Current_Price'].copy()
        X = df_cleaned.drop('Current_Price', axis=1).drop('Date', axis=1).drop('Symbol', axis=1)
        return X, Y

