from src.expense_classifier import ExpenseClassifier
from config import Config

def train_and_save_model():
    """Train the model and save it"""
    classifier = ExpenseClassifier()
    classifier.train()
    classifier.save_model(Config.MODEL_PATH)
    print("Model trained and saved!")

if __name__ == '__main__':
    train_and_save_model()