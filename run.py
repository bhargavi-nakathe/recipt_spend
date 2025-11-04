#!/usr/bin/env python3
"""
Main entry point for the Receipt Spending Classifier
"""

import os
import sys
from src.expense_tracker import ExpenseTracker
from src.expense_classifier import ExpenseClassifier
from config import Config

def main():
    """Initialize and test all components"""
    print("🚀 Initializing Receipt Spending Classifier...")
    
    # Initialize database
    print("📊 Setting up database...")
    tracker = ExpenseTracker()
    print("✅ Database initialized successfully!")
    
    # Train and save model
    print("🤖 Training classification model...")
    classifier = ExpenseClassifier()
    classifier.train()
    classifier.save_model(Config.MODEL_PATH)
    print("✅ Model trained and saved!")
    
    print("\n🎉 All systems ready!")
    print("👉 Run 'python app.py' to start the web application")

if __name__ == "__main__":
    main()