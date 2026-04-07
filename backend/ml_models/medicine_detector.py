import cv2
import numpy as np
from PIL import Image
import io

class MedicineDetector:
    """
    Uses image processing and pattern recognition to detect fake medicines
    """
    def __init__(self):
        self.authentic_patterns = {
            'hologram': False,
            'barcode_valid': False,
            'colors_consistent': False,
            'text_clear': False
        }
    
    def verify(self, image_file):
        """Verify medicine authenticity from image"""
        try:
            # Read image
            image = Image.open(image_file)
            img_array = np.array(image)
            
            # Convert to OpenCV format
            if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
            else:
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Analyze image features
            results = self.analyze_medicine_features(img_cv)
            
            # Calculate confidence
            confidence = sum(results.values()) / len(results) * 100
            is_authentic = confidence > 70
            
            return {
                'is_authentic': is_authentic,
                'confidence': confidence / 100,
                'details': {
                    'hologram_detected': results['hologram'],
                    'barcode_valid': results['barcode_valid'],
                    'color_consistency': results['colors_consistent'],
                    'text_clarity': results['text_clear']
                }
            }
        except Exception as e:
            return {
                'is_authentic': False,
                'confidence': 0,
                'details': {'error': str(e)}
            }
    
    def analyze_medicine_features(self, img):
        """Analyze various features of the medicine image"""
        features = {
            'hologram': self.detect_hologram(img),
            'barcode_valid': self.check_barcode_quality(img),
            'colors_consistent': self.check_color_consistency(img),
            'text_clear': self.check_text_clarity(img)
        }
        return features
    
    def detect_hologram(self, img):
        """Detect if image has holographic properties"""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        return np.mean(saturation) > 100
    
    def check_barcode_quality(self, img):
        """Check barcode visibility and quality"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return len(contours) > 5
    
    def check_color_consistency(self, img):
        """Check if colors are consistent (not faded/altered)"""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_variance = np.std(hsv[:, :, 2])
        return color_variance > 30
    
    def check_text_clarity(self, img):
        """Check text clarity and sharpness"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var > 100

# Create global detector instance
detector = MedicineDetector()

def verify_medicine(image_file):
    """Public function to verify medicine"""
    return detector.verify(image_file)
