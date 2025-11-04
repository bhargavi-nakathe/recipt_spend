from src.expense_tracker import ExpenseTracker

def setup_database():
    """Initialize the database"""
    tracker = ExpenseTracker()
    print("Database setup completed!")

if __name__ == '__main__':
    setup_database()