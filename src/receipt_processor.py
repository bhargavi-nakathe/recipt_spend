import cv2
import pytesseract
import re
import numpy as np
from PIL import Image
from config import Config

class ReceiptProcessor:
    def __init__(self):
        self.categories = Config.CATEGORIES
    
    def preprocess_image(self, image_path):
        """Enhance image for better OCR accuracy"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            denoised = cv2.medianBlur(gray, 5)
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return thresh
        except Exception as e:
            print(f"Error in image preprocessing: {e}")
            return None
    
    def extract_text(self, image_path):
        """Extract text from receipt image"""
        try:
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return ""
            
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            return text
        except Exception as e:
            print(f"Error in OCR: {e}")
            return ""
    
    def parse_receipt_text(self, text):
        """Parse extracted text to identify items and prices"""
        items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for price patterns
            price_patterns = [
                r'(\d+\.\d{2})\s*$',  # 10.99 at end
                r'\$(\d+\.\d{2})',    # $10.99
                r'(\d+\.\d{2})\s*[A-Za-z]',  # 10.99 followed by text
            ]
            
            for pattern in price_patterns:
                price_match = re.search(pattern, line)
                if price_match:
                    try:
                        price = float(price_match.group(1))
                        # Extract item name (everything before price)
                        item_name = re.sub(pattern, '', line).strip()
                        if item_name and price > 0:
                            items.append({
                                'name': item_name,
                                'price': price,
                                'original_text': line
                            })
                        break
                    except ValueError:
                        continue
        
        return items