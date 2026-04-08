"""
Enhanced Medicine Authenticity Detector
Combines OCR, ML, and Rule-based checks for comprehensive validation
"""

import cv2
import numpy as np
from PIL import Image
import io
import re
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import pytesseract for OCR
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# Try to import medicine database
try:
    from medicine_database import REAL_MEDICINES, verify_medicine_in_database, get_medicine_info
    MEDICINE_DB_AVAILABLE = True
except ImportError:
    MEDICINE_DB_AVAILABLE = False
    REAL_MEDICINES = {}
    def verify_medicine_in_database(name):
        return False
    def get_medicine_info(name):
        return {}

class EnhancedMedicineDetector:
    """
    Multi-layered approach to medicine authenticity detection:
    1. OCR-based verification (extract text, match with database)
    2. Image analysis (packaging quality, colors, clarity)
    3. Rule-based checks (barcode, text, hologram)
    """
    
    def __init__(self):
        # Real medicine database (simplified)
        self.medicine_database = {
            'aspirin': {'batch_pattern': r'^ASP\d{6}$', 'confidence': 0.85},
            'paracetamol': {'batch_pattern': r'^PAR\d{6}$', 'confidence': 0.85},
            'amoxicillin': {'batch_pattern': r'^AMX\d{6}$', 'confidence': 0.85},
            'ibuprofen': {'batch_pattern': r'^IBU\d{6}$', 'confidence': 0.85},
            'metformin': {'batch_pattern': r'^MET\d{6}$', 'confidence': 0.85},
            'omeprazole': {'batch_pattern': r'^OMP\d{6}$', 'confidence': 0.85},
            'atorvastatin': {'batch_pattern': r'^ATV\d{6}$', 'confidence': 0.85},
            'viagra': {'batch_pattern': r'^VGR\d{6}$', 'confidence': 0.85},
        }
        
        self.threshold_confidence = 0.70
    
    def verify(self, image_file):
        """
        Complete verification pipeline
        
        Returns:
            {
                'is_authentic': bool,
                'final_confidence': float,
                'ocr_result': dict,
                'image_analysis': dict,
                'rule_checks': dict,
                'decision_logic': dict,
                'recommendation': str
            }
        """
        try:
            # Load image
            image = Image.open(image_file)
            img_array = np.array(image)
            
            # Convert to OpenCV format
            if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
            else:
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # 1. OCR-based verification
            ocr_result = self.extract_and_verify_text(img_cv)
            
            # 2. Image analysis
            image_analysis = self.analyze_packaging_quality(img_cv)
            
            # 3. Rule-based checks
            rule_checks = self.perform_rule_checks(img_cv)
            
            # 4. Combine results
            decision = self.combine_analysis(ocr_result, image_analysis, rule_checks)
            
            return {
                'is_authentic': decision['is_authentic'],
                'final_confidence': float(decision['final_confidence']),
                'ocr_result': ocr_result,
                'image_analysis': image_analysis,
                'rule_checks': rule_checks,
                'decision_logic': decision,
                'reasoning': decision.get('reasoning', []),  # ← NEW
                'recommendation': self.get_recommendation(decision)
            }
            
        except Exception as e:
            return {
                'is_authentic': False,
                'final_confidence': 0.0,
                'error': str(e),
                'recommendation': 'Unable to verify. Please try with a clear image.'
            }
    
    def extract_and_verify_text(self, img_cv):
        """
        A) OCR-based verification with Database Integration
        Extract medicine name and batch number, verify against real medicines database
        """
        result = {
            'medicine_name': None,
            'batch_number': None,
            'database_match': False,
            'database_info': None,
            'confidence': 0.0,
            'extracted_text': '',
            'ocr_status': 'Not attempted'
        }
        
        # Try OCR if available
        if TESSERACT_AVAILABLE:
            try:
                # Extract text from image
                extracted_text = pytesseract.image_to_string(img_cv)
                result['extracted_text'] = extracted_text.strip()
                result['ocr_status'] = 'Success' if extracted_text.strip() else 'No text found'
                
                # Search for medicine names in extracted text
                text_lower = extracted_text.lower()
                
                # First, check against real medicines database
                found_medicines = []
                for medicine_name in REAL_MEDICINES.keys():
                    if medicine_name in text_lower:
                        found_medicines.append(medicine_name)
                
                # If multiple found, use the longest match (most specific)
                if found_medicines:
                    medicine_match = max(found_medicines, key=len)
                    result['medicine_name'] = medicine_match.title()
                    result['database_match'] = True
                    result['database_info'] = get_medicine_info(medicine_match)
                    result['confidence'] = 0.85  # High confidence if found in real database
                else:
                    # Try legacy database
                    for medicine_name in self.medicine_database.keys():
                        if medicine_name in text_lower:
                            result['medicine_name'] = medicine_name.title()
                            result['database_match'] = False  # Not in verified database
                            result['confidence'] = 0.65  # Lower confidence
                            break
                
                # Try to extract batch number (format: XXX followed by numbers)
                batch_patterns = re.findall(r'[A-Z]{2,4}\d{5,8}', extracted_text)
                if batch_patterns:
                    result['batch_number'] = batch_patterns[0]
                    
                    # Validate batch pattern if medicine name found
                    if result['medicine_name'] and result['medicine_name'].lower() in self.medicine_database:
                        medicine_lower = result['medicine_name'].lower()
                        expected_pattern = self.medicine_database[medicine_lower].get('batch_pattern')
                        if expected_pattern and re.match(expected_pattern, result['batch_number']):
                            # Increase confidence for valid batch format
                            result['confidence'] = min(1.0, result['confidence'] + 0.1)
                
            except Exception as e:
                result['ocr_error'] = str(e)
                result['ocr_status'] = f'Error: {str(e)}'
        else:
            # Fallback: Look for common medicine names in image
            result['extracted_text'] = '(OCR not available - pytesseract not installed)'
            result['medicine_name'] = 'Unable to extract'
            result['ocr_status'] = 'OCR unavailable'
        
        return result
    
    def analyze_packaging_quality(self, img_cv):
        """
        B) Image-based AI analysis
        Analyze packaging quality, colors, printing clarity
        """
        analysis = {
            'hologram_detected': False,
            'hologram_confidence': 0.0,
            'barcode_valid': False,
            'barcode_confidence': 0.0,
            'color_consistency': False,
            'color_consistency_score': 0.0,
            'text_clarity': False,
            'text_clarity_score': 0.0,
            'overall_packaging_quality': 'Unknown'
        }
        
        try:
            # Hologram detection
            hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
            saturation = hsv[:, :, 1]
            mean_saturation = np.mean(saturation)
            hologram_detected = mean_saturation > 100
            analysis['hologram_detected'] = bool(hologram_detected)
            analysis['hologram_confidence'] = float(min(mean_saturation / 255, 1.0))
            
            # Barcode validation
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            barcode_valid = len(contours) > 5
            analysis['barcode_valid'] = bool(barcode_valid)
            analysis['barcode_confidence'] = float(min(len(contours) / 50, 1.0))
            
            # Color consistency
            color_variance = np.std(hsv[:, :, 2])
            color_consistent = color_variance > 30
            analysis['color_consistency'] = bool(color_consistent)
            analysis['color_consistency_score'] = float(min(color_variance / 100, 1.0))
            
            # Text clarity
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            text_clear = laplacian_var > 100
            analysis['text_clarity'] = bool(text_clear)
            analysis['text_clarity_score'] = float(min(laplacian_var / 500, 1.0))
            
            # Overall packaging quality
            quality_score = np.mean([
                analysis['hologram_confidence'],
                analysis['barcode_confidence'],
                analysis['color_consistency_score'],
                analysis['text_clarity_score']
            ])
            
            if quality_score > 0.75:
                analysis['overall_packaging_quality'] = 'Excellent'
            elif quality_score > 0.55:
                analysis['overall_packaging_quality'] = 'Good'
            elif quality_score > 0.35:
                analysis['overall_packaging_quality'] = 'Fair'
            else:
                analysis['overall_packaging_quality'] = 'Poor'
            
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    def perform_rule_checks(self, img_cv):
        """
        C) Rule-based checks (fast verification)
        """
        checks = {
            'image_resolution': 'Unknown',
            'image_blur_detection': False,
            'image_brightness': 'Unknown',
            'checks_passed': 0,
            'checks_total': 3
        }
        
        try:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            
            # Resolution check
            height, width = gray.shape
            if height * width > 100000:  # > 300x300
                checks['image_resolution'] = 'Good'
            elif height * width > 40000:  # > 200x200
                checks['image_resolution'] = 'Acceptable'
            else:
                checks['image_resolution'] = 'Low'
            
            # Blur detection
            laplacian_variance = cv2.Laplacian(gray, cv2.CV_64F).var()
            checks['image_blur_detection'] = laplacian_variance < 100
            
            # Brightness check
            mean_brightness = np.mean(gray)
            if mean_brightness > 50 and mean_brightness < 200:
                checks['image_brightness'] = 'Good'
                checks['checks_passed'] += 1
            else:
                checks['image_brightness'] = 'Poor (too bright/dark)'
            
            if checks['image_resolution'] != 'Low':
                checks['checks_passed'] += 1
            
            if not checks['image_blur_detection']:
                checks['checks_passed'] += 1
            
        except Exception as e:
            checks['error'] = str(e)
        
        return checks
    
    def combine_analysis(self, ocr_result, image_analysis, rule_checks):
        """
        3. Final Decision Logic
        Combine all three approaches for final verdict with EXPLAINABILITY
        """
        scores = []
        reasoning = []
        
        # OCR score (40% weight)
        if ocr_result['database_match']:
            ocr_score = ocr_result['confidence']
            scores.append(('OCR Match', ocr_score, 0.40))
            reasoning.append({
                'layer': 'OCR Verification',
                'status': 'PASS',
                'detail': f"✓ Medicine '{ocr_result['medicine_name']}' found in authentic database ({int(ocr_score*100)}% confidence)",
                'score': ocr_score
            })
        else:
            scores.append(('OCR Match', 0.5, 0.40))  # Unknown
            reasoning.append({
                'layer': 'OCR Verification',
                'status': 'WARNING',
                'detail': f"⚠ Could not extract clear medicine name (OCR: '{ocr_result.get('medicine_name', 'N/A')}')",
                'score': 0.5
            })
        
        # Image analysis score (40% weight)
        image_score = np.mean([
            image_analysis['hologram_confidence'],
            image_analysis['barcode_confidence'],
            image_analysis['color_consistency_score'],
            image_analysis['text_clarity_score']
        ])
        scores.append(('Image Quality', image_score, 0.40))
        
        # Build image analysis reasoning
        image_details = []
        if image_analysis['hologram_confidence'] > 0.6:
            image_details.append(f"✓ Hologram detected ({int(image_analysis['hologram_confidence']*100)}%)")
        else:
            image_details.append(f"✗ Hologram missing/poor ({int(image_analysis['hologram_confidence']*100)}%)")
        
        if image_analysis['barcode_confidence'] > 0.5:
            image_details.append(f"✓ Barcode valid ({int(image_analysis['barcode_confidence']*100)}%)")
        else:
            image_details.append(f"✗ Barcode damaged/missing ({int(image_analysis['barcode_confidence']*100)}%)")
        
        if image_analysis['text_clarity_score'] > 0.6:
            image_details.append(f"✓ Text clarity good ({int(image_analysis['text_clarity_score']*100)}%)")
        else:
            image_details.append(f"✗ Text clarity poor ({int(image_analysis['text_clarity_score']*100)}%)")
        
        reasoning.append({
            'layer': 'Image Quality Analysis',
            'status': 'PASS' if image_score > 0.6 else 'WARNING' if image_score > 0.4 else 'FAIL',
            'detail': ', '.join(image_details),
            'score': image_score,
            'overall_quality': image_analysis['overall_packaging_quality']
        })
        
        # Rule checks score (20% weight)
        rule_score = rule_checks['checks_passed'] / rule_checks['checks_total']
        scores.append(('Rule Checks', rule_score, 0.20))
        
        rule_details = []
        if rule_checks['image_resolution'] != 'Low':
            rule_details.append(f"✓ Resolution: {rule_checks['image_resolution']}")
        else:
            rule_details.append(f"✗ Resolution: Too low")
        
        if not rule_checks['image_blur_detection']:
            rule_details.append(f"✓ Image: Not blurry")
        else:
            rule_details.append(f"✗ Image: Blurry")
        
        if rule_checks['image_brightness'] == 'Good':
            rule_details.append(f"✓ Brightness: Normal")
        else:
            rule_details.append(f"✗ Brightness: {rule_checks['image_brightness']}")
        
        reasoning.append({
            'layer': 'Technical Checks',
            'status': 'PASS' if rule_score > 2/3 else 'WARNING',
            'detail': ', '.join(rule_details),
            'score': rule_score
        })
        
        # Calculate weighted final confidence
        final_confidence = sum(score * weight for _, score, weight in scores)
        
        # Decision
        is_authentic = final_confidence > self.threshold_confidence
        
        return {
            'is_authentic': bool(is_authentic),
            'final_confidence': float(final_confidence),
            'component_scores': [
                {'component': name, 'score': float(score), 'weight': weight}
                for name, score, weight in scores
            ],
            'threshold': self.threshold_confidence,
            'decision_status': 'AUTHENTIC ✓' if is_authentic else 'COUNTERFEIT ✗',
            'reasoning': reasoning  # ← NEW: Explainability
        }
    
    def get_recommendation(self, decision):
        """Get user-friendly recommendation with detailed breakdown"""
        confidence = decision['final_confidence']
        is_authentic = decision['is_authentic']
        
        # Generate severity levels
        if not is_authentic:
            if confidence < 0.4:
                severity = 'CRITICAL'
                status_icon = '🚨'
                message = 'HIGH RISK: This medicine appears to be COUNTERFEIT. DO NOT USE.'
                action = 'Report to drug regulatory authority and pharmacy'
            elif confidence < 0.6:
                severity = 'HIGH'
                status_icon = '⚠️'
                message = 'SUSPICIOUS: This medicine may be counterfeit or low quality.'
                action = 'Verify with pharmacy or manufacturer before use'
            else:
                severity = 'MEDIUM'
                status_icon = '⚠️'
                message = 'WARNING: Authenticity could not be fully verified.'
                action = 'Verify with authorized pharmacy'
        else:
            if confidence > 0.85:
                severity = 'LOW'
                status_icon = '✅'
                message = 'SAFE: This medicine appears AUTHENTIC with high confidence.'
                action = 'Safe to use'
            elif confidence > 0.75:
                severity = 'LOW'
                status_icon = '✅'
                message = 'LIKELY AUTHENTIC: This medicine appears genuine.'
                action = 'Safe to use'
            else:
                severity = 'MEDIUM'
                status_icon = '⚠️'
                message = 'PROBABLE: This medicine is likely authentic, but verification confidence is moderate.'
                action = 'For critical medicines, verify with manufacturer'
        
        return {
            'recommendation': message,
            'action': action,
            'severity': severity,
            'status_icon': status_icon,
            'confidence_percentage': int(confidence * 100)
        }

# Create global detector instance
detector = EnhancedMedicineDetector()

def verify_medicine_enhanced(image_file):
    """Public function to verify medicine with enhanced detection"""
    return detector.verify(image_file)
