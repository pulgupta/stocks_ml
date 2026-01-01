from model_trainer import ModelTrainer
from data_processor import DataProcessor
import pandas as pd


class Predictor:

    def predict_from_csv(self, csv_path, model_name, models_dir):
        """
        Load a CSV file and predict stock prices using trained model.
        """
        print(f"\n{'='*50}")
        print(f"PREDICTING PRICES FROM: {csv_path}")
        print(f"{'='*50}\n")

        # Load model
        model_trainer = ModelTrainer()
        model, scaler, metadata = model_trainer.load_model(model_name, models_dir)
        feature_columns = metadata['feature_columns']

        # Load CSV
        X = pd.read_csv(csv_path)
        print(f"Loaded {len(X)} rows from CSV")

        # Scale features
        x_scaled = scaler.transform(X)

        # Make predictions
        predictions = model.predict(x_scaled)
        print(f'Prediction is {predictions}')
        return predictions