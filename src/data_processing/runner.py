import argparse
from pathlib import Path

from data_fetcher import DataFetcher
from data_processor import DataProcessor
from model_trainer import ModelTrainer
from predictor import Predictor


def main():
    root_dir = str(Path(__file__).resolve().parent.parent.parent)
    print('Root dir:', root_dir)
    parser = argparse.ArgumentParser(
        description='Train or predict stock prices using ML',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Train command
    subparsers.add_parser('train', help='Train a new model')
    subparsers.add_parser('fetch_data', help='Fetch data')

    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Predict prices from CSV')
    predict_parser.add_argument('--ticker', required=True, help='CSV file to predict')

    args = parser.parse_args()

    if args.command == 'fetch_data':
        print('Fetching data')
        data_fetcher = DataFetcher()
        data_fetcher.fetch_all_data(root_dir)
    elif args.command == 'train':
        print('Train a new model')
        data_processor = DataProcessor()
        X, Y = data_processor.prepare_data(root_dir + '/data/raw')
        model_trainer = ModelTrainer()
        model_trainer.train(X, Y, root_dir + '/models/saved_models')
    elif args.command == 'predict':
        print('Predict prices')
        predictor = Predictor()
        predictor.predict(args.ticker, 'random_forest', root_dir + '/models/saved_models')


if __name__ == "__main__":
    main()
