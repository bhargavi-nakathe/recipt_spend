import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    DATABASE_PATH = 'expenses.db'
    MODEL_PATH = 'models/trained_model.pkl'
    
    # Allowed extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    
    # Categories for classification
    CATEGORIES = {
        'food': ['restaurant', 'cafe', 'food', 'meal', 'dining', 'coffee', 'pizza', 'burger'],
        'groceries': ['grocery', 'supermarket', 'market', 'vegetables', 'fruits', 'milk', 'bread', 'eggs'],
        'utilities': ['electricity', 'water', 'gas', 'internet', 'phone', 'bill', 'payment'],
        'transport': ['fuel', 'gasoline', 'bus', 'train', 'taxi', 'uber', 'ride'],
        'entertainment': ['movie', 'cinema', 'concert', 'game', 'netflix', 'spotify', 'subscription'],
        'shopping': ['clothes', 'electronics', 'fashion', 'accessories', 'store']
    }

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS