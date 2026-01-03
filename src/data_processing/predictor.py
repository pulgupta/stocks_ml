from model_trainer import ModelTrainer
from data_fetcher import DataFetcher
import pandas as pd


class Predictor:

    def predict(self, ticker, model_name, models_dir):
        data_fetcher = DataFetcher()
        data = data_fetcher.get_comprehensive_stock_data(data_fetcher.modify_ticker(ticker))
        print(f"\n{'='*50}")
        print(f"PREDICTING PRICES FROM: {ticker}")
        print(f"{'='*50}\n")

        # Load model
        model_trainer = ModelTrainer()
        model, scaler, metadata = model_trainer.load_model(model_name, models_dir)
        feature_columns = metadata['feature_columns']

        # Load CSV
        X = pd.DataFrame([data['current_fundamentals']])[feature_columns]
        print(f"Loaded {len(X)} rows from CSV")

        # Scale features
        x_scaled = scaler.transform(X)

        # Make predictions
        predictions = model.predict(x_scaled)
        print(f'Prediction is {predictions}')
        return predictions