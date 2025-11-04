import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
from config import Config

class ExpenseClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        self.classifier = RandomForestClassifier(n_estimators=50, random_state=42)
        self.is_trained = False
    
    def get_training_data(self):
        """Generate training data"""
        training_data = [
            # Groceries
            ("milk bread eggs", "groceries"),
            ("chicken rice vegetables", "groceries"),
            ("fruit banana apple", "groceries"),
            ("supermarket grocery", "groceries"),
            
            # Food
            ("pizza burger restaurant", "food"),
            ("coffee cafe starbucks", "food"),
            ("dining dinner lunch", "food"),
            ("fast food meal", "food"),
            
            # Utilities
            ("electricity bill payment", "utilities"),
            ("water bill utility", "utilities"),
            ("internet phone bill", "utilities"),
            
            # Transport
            ("gasoline fuel shell", "transport"),
            ("uber taxi ride", "transport"),
            ("bus train transit", "transport"),
            
            # Entertainment
            ("movie cinema tickets", "entertainment"),
            ("netflix subscription", "entertainment"),
            
            # Shopping
            ("shirt pants fashion", "shopping"),
            ("electronics phone", "shopping"),
        ]
        
        texts = [data[0] for data in training_data]
        labels = [data[1] for data in training_data]
        
        return texts, labels
    
    def train(self):
        """Train the classifier"""
        texts, labels = self.get_training_data()
        
        X = self.vectorizer.fit_transform(texts)
        y = labels
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.classifier.fit(X_train, y_train)
        self.is_trained = True
        
        # Test accuracy
        train_accuracy = self.classifier.score(X_train, y_train)
        test_accuracy = self.classifier.score(X_test, y_test)
        
        print(f"Training completed - Train Accuracy: {train_accuracy:.2f}, Test Accuracy: {test_accuracy:.2f}")
        
        return self
    
    def predict(self, text):
        """Predict category for text"""
        if not self.is_trained:
            self.train()
        
        features = self.vectorizer.transform([text])
        prediction = self.classifier.predict(features)[0]
        probability = max(self.classifier.predict_proba(features)[0])
        
        return prediction, probability
    
    def save_model(self, filepath):
        """Save trained model"""
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'is_trained': True
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath):
        """Load trained model"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.vectorizer = model_data['vectorizer']
            self.classifier = model_data['classifier']
            self.is_trained = model_data['is_trained']
        else:
            self.train()
            self.save_model(filepath)