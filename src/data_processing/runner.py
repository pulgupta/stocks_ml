from data_processor import DataProcessor
from model_trainer import ModelTrainer
from predictor import Predictor
import argparse

def main():

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
        model_trainer = ModelTrainer()
        model_trainer.train(args)
    else:

if __name__ == "__main__":
    main()