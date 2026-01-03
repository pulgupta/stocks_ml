from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np
import json

class ModelTrainer:

    def train(self, X, Y, path):
        X_train, X_test, y_train, y_test = train_test_split(
            X, Y, test_size=0.2, random_state=42
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train_scaled, y_train)

        y_pred = model.predict(X_test_scaled)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)  # Calculate RMSE manually
        r2 = r2_score(y_test, y_pred)

        print(f"\n{'='*50}")
        print("MODEL PERFORMANCE")
        print(f"{'='*50}")
        print(f"MAE: ₹{mae:.2f}")
        print(f"RMSE: ₹{rmse:.2f}")
        print(f"R² Score: {r2:.4f}")
        print(f"Mean Absolute Error %: {(mae / y_test.mean()) * 100:.2f}%")

        self.save_model(model, scaler, X.columns, 'random_forest', path)

    def save_model(self, model, scaler, feature_columns, model_name, output_dir):
        """
        Save trained model, scaler, and metadata.
        """
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)

        # Save model
        model_path = Path(output_dir) / f'{model_name}_model.joblib'
        joblib.dump(model, model_path)
        print(f"✓ Model saved to: {model_path}")

        # Save scaler
        scaler_path = Path(output_dir) / f'{model_name}_scaler.joblib'
        joblib.dump(scaler, scaler_path)
        print(f"✓ Scaler saved to: {scaler_path}")

        # Save metadata (feature columns)
        metadata = {
            'feature_columns': feature_columns.tolist(),
            'model_type': type(model).__name__
        }
        metadata_path = Path(output_dir) / f'{model_name}_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Metadata saved to: {metadata_path}")

        return model_path, scaler_path, metadata_path

    def load_model(self, model_name, models_dir):
        """
        Load trained model, scaler, and metadata.
        """
        models_path = Path(models_dir)

        # Load model
        model_path = models_path / f'{model_name}_model.joblib'
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        model = joblib.load(model_path)
        print(f"✓ Model loaded from: {model_path}")

        # Load scaler
        scaler_path = models_path / f'{model_name}_scaler.joblib'
        if not scaler_path.exists():
            raise FileNotFoundError(f"Scaler not found: {scaler_path}")
        scaler = joblib.load(scaler_path)
        print(f"✓ Scaler loaded from: {scaler_path}")

        # Load metadata
        metadata_path = models_path / f'{model_name}_metadata.json'
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found: {metadata_path}")
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        print(f"✓ Metadata loaded from: {metadata_path}")

        return model, scaler, metadata

