from data_processor import DataProcessor
from model_trainer import ModelTrainer
from predictor import Predictor
import argparse
from pathlib import Path
import os

def main():

    ROOT_DIR = Path(__file__).resolve().parent.parent.parent

    parser = argparse.ArgumentParser(
        description='Train or predict stock prices using ML',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Train command
    train_parser = subparsers.add_parser('train', help='Train a new model')

    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Predict prices from CSV')
    predict_parser.add_argument('--input', required=True, help='CSV file to predict')

    args = parser.parse_args()

    if args.command == 'train':
        data_processor = DataProcessor()
        X, Y = data_processor.prepare_data(str(ROOT_DIR) + '/data/raw')
        model_trainer = ModelTrainer()
        model_trainer.train(X, Y)
    else:
        predictor = Predictor()
        predictor.predict_from_csv(args.input)

if __name__ == "__main__":
    main()