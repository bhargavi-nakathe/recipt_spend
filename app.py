from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from config import Config, allowed_file
from src.receipt_processor import ReceiptProcessor
from src.expense_classifier import ExpenseClassifier
from src.expense_tracker import ExpenseTracker

# Initialize components
app = Flask(__name__)
app.config.from_object(Config)

processor = ReceiptProcessor()
classifier = ExpenseClassifier()
tracker = ExpenseTracker()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_receipt():
    if 'receipt' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process receipt
            text = processor.extract_text(filepath)
            items = processor.parse_receipt_text(text)
            
            # Classify items
            classified_items = []
            total_amount = 0
            
            for item in items:
                category, confidence = classifier.predict(item['name'])
                classified_item = {
                    'name': item['name'],
                    'amount': item['price'],
                    'category': category,
                    'confidence': round(confidence * 100, 1)
                }
                classified_items.append(classified_item)
                total_amount += item['price']
            
            # Save to database
            receipt_id = tracker.save_receipt(filename, total_amount, classified_items)
            
            return jsonify({
                'success': True,
                'receipt_id': receipt_id,
                'total_amount': total_amount,
                'items': classified_items,
                'items_count': len(classified_items)
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/analytics')
def get_analytics():
    days = request.args.get('days', 30, type=int)
    summary = tracker.get_spending_summary(days)
    return jsonify(summary)

@app.route('/api/recommendations')
def get_recommendations():
    recommendations = tracker.get_recommendations()
    return jsonify(recommendations)

@app.route('/api/recent-expenses')
def get_recent_expenses():
    # Implement recent expenses endpoint
    return jsonify({'recent': []})

if __name__ == '__main__':
    # Train model on startup
    classifier.load_model(Config.MODEL_PATH)
    app.run(debug=True, host='0.0.0.0', port=5000)