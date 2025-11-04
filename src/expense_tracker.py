import sqlite3
import json
from datetime import datetime, timedelta
from config import Config

class ExpenseTracker:
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.model_path = Config.MODEL_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS receipts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    total_amount REAL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receipt_id INTEGER,
                    item_name TEXT,
                    category TEXT,
                    amount REAL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (receipt_id) REFERENCES receipts (id)
                )
            ''')
            
            conn.commit()
    
    def save_receipt(self, filename, total_amount, items):
        """Save receipt and items to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Save receipt
            cursor.execute(
                'INSERT INTO receipts (filename, total_amount) VALUES (?, ?)',
                (filename, total_amount)
            )
            receipt_id = cursor.lastrowid
            
            # Save items
            for item in items:
                cursor.execute(
                    '''INSERT INTO expenses 
                    (receipt_id, item_name, category, amount) 
                    VALUES (?, ?, ?, ?)''',
                    (receipt_id, item['name'], item['category'], item['amount'])
                )
            
            conn.commit()
            return receipt_id
    
    def get_spending_summary(self, days=30):
        """Get spending summary for given period"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Category breakdown
            cursor.execute('''
                SELECT category, SUM(amount) as total
                FROM expenses
                WHERE date >= datetime('now', ?)
                GROUP BY category
            ''', (f'-{days} days',))
            
            category_data = dict(cursor.fetchall())
            
            # Total spending
            total_spending = sum(category_data.values())
            
            return {
                'categories': category_data,
                'total': total_spending,
                'period_days': days
            }
    
    def get_recommendations(self):
        """Generate savings recommendations"""
        summary = self.get_spending_summary(30)
        categories = summary['categories']
        total = summary['total']
        
        recommendations = []
        
        # Analyze spending patterns
        for category, amount in categories.items():
            percentage = (amount / total) * 100 if total > 0 else 0
            
            if category == 'food' and percentage > 30:
                recommendations.append({
                    'category': category,
                    'message': f'You spend {percentage:.1f}% on food. Try cooking at home more!',
                    'savings_tip': 'Meal prep can save 20-30% on food costs'
                })
            
            elif category == 'entertainment' and percentage > 15:
                recommendations.append({
                    'category': category,
                    'message': f'Entertainment is {percentage:.1f}% of spending.',
                    'savings_tip': 'Look for free community events'
                })
        
        if not recommendations:
            recommendations.append({
                'category': 'general',
                'message': 'Your spending looks balanced!',
                'savings_tip': 'Keep tracking to maintain good habits'
            })
        
        return recommendations
    