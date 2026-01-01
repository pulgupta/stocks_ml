from model_trainer import ModelTrainer
from data_processor import DataProcessor
import pandas as pd


class Predictor:

    def predict_from_csv(csv_path, model_name, models_dir):
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
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from CSV")

        # Prepare features (no target needed for prediction)
        data_processor = DataProcessor()
        X, Y = data_processor.prepare_data(df, feature_columns=feature_columns)

        # Scale features
        X_scaled = scaler.transform(X)

        # Make predictions
        predictions = model.predict(X_scaled)
        print(f'Prediction is {predictions}')
        return predictions