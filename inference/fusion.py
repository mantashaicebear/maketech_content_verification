"""
Fusion Classifier for Content Verification
"""

import numpy as np
from typing import Dict, List

class FusionClassifier:
    """Fuse text and image predictions"""
    
    def __init__(self):
        self.category_mapping = {
            'food': 'food',
            'tech': 'tech', 
            'education': 'education',
            'health': 'health',
            'finance': 'finance',
            'fashion': 'fashion',
            'electronics': 'electronics',
            'automotive': 'automotive',
            'real_estate': 'real_estate',
            'entertainment': 'entertainment',
            'weapons': 'weapons',
            'drugs': 'drugs',
            'adult_content': 'adult_content',
            'gambling': 'gambling',
            'document': 'education',
            'person': 'other',
            'nature': 'other',
            'vehicle': 'automotive',
            'other': 'other'
        }
    
    def fuse_predictions(self, text_prediction: Dict, image_predictions: List[Dict]) -> Dict:
        """Fuse text and image predictions"""
        try:
            # If no predictions, return unknown
            if not text_prediction and not image_predictions:
                return {
                    'category': 'unknown',
                    'confidence': 0.0,
                    'is_restricted': False
                }
            
            # If only text
            if text_prediction and not image_predictions:
                return text_prediction
            
            # If only images
            if not text_prediction and image_predictions:
                # Use highest confidence image prediction
                best_image = max(image_predictions, key=lambda x: x.get('confidence', 0))
                return best_image
            
            # Both text and images available
            text_category = text_prediction.get('category', 'unknown')
            text_confidence = text_prediction.get('confidence', 0.0)
            
            # Get best image prediction
            best_image = max(image_predictions, key=lambda x: x.get('confidence', 0))
            image_category = best_image.get('category', 'unknown')
            image_confidence = best_image.get('confidence', 0.0)
            
            # Map categories to common ones
            mapped_text_cat = self.category_mapping.get(text_category, text_category)
            mapped_image_cat = self.category_mapping.get(image_category, image_category)
            
            # Weighted fusion (text: 0.7, image: 0.3)
            if mapped_text_cat == mapped_image_cat:
                # Same category - average confidence
                final_category = mapped_text_cat
                final_confidence = (text_confidence * 0.7 + image_confidence * 0.3)
            else:
                # Different categories - choose higher confidence
                if text_confidence >= image_confidence:
                    final_category = mapped_text_cat
                    final_confidence = text_confidence
                else:
                    final_category = mapped_image_cat
                    final_confidence = image_confidence
            
            # Check if restricted
            is_restricted = text_prediction.get('is_restricted', False) or \
                           any(img.get('is_restricted', False) for img in image_predictions)
            
            return {
                'category': final_category,
                'confidence': float(final_confidence),
                'is_restricted': is_restricted,
                'source': 'fusion',
                'text_prediction': text_prediction,
                'image_predictions': image_predictions
            }
            
        except Exception as e:
            return {
                'category': 'error',
                'confidence': 0.0,
                'is_restricted': False,
                'error': str(e)
            }