"""
Fusion Classifier
Combines text and image predictions
"""

import logging
import numpy as np
from typing import Dict, List, Tuple, Any

logger = logging.getLogger(__name__)

class FusionClassifier:
    """
    Fuses predictions from text and image classifiers
    """
    
    def __init__(self, text_classifier, image_classifier):
        """
        Initialize fusion classifier
        
        Args:
            text_classifier: TextClassifier instance
            image_classifier: ImageClassifier instance
        """
        self.text_classifier = text_classifier
        self.image_classifier = image_classifier
        
        # Mapping between text and image categories
        self.category_mapping = self._create_category_mapping()
        
        logger.info("FusionClassifier initialized")
    
    def _create_category_mapping(self) -> Dict[str, List[str]]:
        """Create mapping between text and image categories"""
        mapping = {
            'food': ['food', 'restaurant', 'meal'],
            'tech': ['tech', 'electronics', 'computer'],
            'weapons': ['weapons', 'firearms', 'guns'],
            'drugs': ['drugs', 'medicine', 'pharmaceutical'],
            'adult_content': ['adult_content', 'explicit'],
            'fashion': ['fashion', 'clothing', 'apparel'],
            'automotive': ['automotive', 'vehicle', 'car'],
            'nature': ['nature', 'animal', 'plant'],
            'document': ['document', 'paper', 'text'],
            'person': ['person', 'face', 'portrait']
        }
        
        # Create reverse mapping
        reverse_mapping = {}
        for main_cat, sub_cats in mapping.items():
            for sub_cat in sub_cats:
                reverse_mapping[sub_cat] = main_cat
        
        return reverse_mapping
    
    def fuse_predictions(
        self,
        text_prediction: Dict,
        image_predictions: List[Dict],
        weights: Dict[str, float] = None
    ) -> Dict:
        """
        Fuse text and image predictions
        
        Args:
            text_prediction: Text prediction result
            image_predictions: List of image prediction results
            weights: Weights for fusion {'text': 0.x, 'image': 0.y}
            
        Returns:
            Fused prediction result
        """
        try:
            # Default weights
            if weights is None:
                weights = {'text': 0.6, 'image': 0.4}
            
            # Normalize weights
            total_weight = weights.get('text', 0) + weights.get('image', 0)
            if total_weight > 0:
                text_weight = weights.get('text', 0) / total_weight
                image_weight = weights.get('image', 0) / total_weight
            else:
                text_weight = image_weight = 0.5
            
            # Process text prediction
            text_category = text_prediction.get('category', 'unknown')
            text_confidence = text_prediction.get('confidence', 0.0)
            
            # Process image predictions
            image_categories = []
            image_confidences = []
            
            for img_pred in image_predictions:
                img_cat = img_pred.get('category', 'unknown')
                img_conf = img_pred.get('confidence', 0.0)
                image_categories.append(img_cat)
                image_confidences.append(img_conf)
            
            # Calculate weighted predictions
            category_scores = {}
            
            # Add text prediction
            mapped_text_cat = self.category_mapping.get(text_category, text_category)
            category_scores[mapped_text_cat] = text_confidence * text_weight
            
            # Add image predictions
            for img_cat, img_conf in zip(image_categories, image_confidences):
                mapped_img_cat = self.category_mapping.get(img_cat, img_cat)
                current_score = category_scores.get(mapped_img_cat, 0)
                category_scores[mapped_img_cat] = current_score + (img_conf * image_weight / len(image_predictions))
            
            # Find best category
            if category_scores:
                best_category = max(category_scores.items(), key=lambda x: x[1])[0]
                best_confidence = category_scores[best_category]
            else:
                best_category = 'unknown'
                best_confidence = 0.0
            
            # Check if any prediction is restricted
            is_restricted = text_prediction.get('is_restricted', False)
            if not is_restricted:
                for img_pred in image_predictions:
                    if img_pred.get('is_restricted', False):
                        is_restricted = True
                        break
            
            # Get top categories
            top_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)[:5]
            
            result = {
                'category': best_category,
                'confidence': float(best_confidence),
                'is_restricted': is_restricted,
                'top_categories': top_categories,
                'fusion_weights': {
                    'text': text_weight,
                    'image': image_weight
                },
                'source_predictions': {
                    'text': {
                        'category': text_category,
                        'confidence': text_confidence
                    },
                    'images': [
                        {
                            'category': img_pred.get('category'),
                            'confidence': img_pred.get('confidence')
                        }
                        for img_pred in image_predictions
                    ]
                }
            }
            
            logger.info(f"Fusion result: {best_category} (confidence: {best_confidence:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in fusion: {e}")
            return {
                'category': 'unknown',
                'confidence': 0.0,
                'is_restricted': False,
                'error': str(e)
            }
    
    def weighted_fusion(
        self,
        predictions: List[Dict],
        weights: List[float] = None
    ) -> Dict:
        """
        Weighted fusion of multiple predictions
        
        Args:
            predictions: List of prediction dictionaries
            weights: List of weights for each prediction
            
        Returns:
            Fused prediction result
        """
        try:
            if not predictions:
                return {'category': 'unknown', 'confidence': 0.0}
            
            # Default weights
            if weights is None:
                weights = [1.0 / len(predictions)] * len(predictions)
            
            # Normalize weights
            total_weight = sum(weights)
            if total_weight > 0:
                weights = [w / total_weight for w in weights]
            else:
                weights = [1.0 / len(predictions)] * len(predictions)
            
            # Aggregate predictions
            category_scores = {}
            
            for pred, weight in zip(predictions, weights):
                category = pred.get('category', 'unknown')
                confidence = pred.get('confidence', 0.0)
                
                current_score = category_scores.get(category, 0)
                category_scores[category] = current_score + (confidence * weight)
            
            # Find best category
            best_category = max(category_scores.items(), key=lambda x: x[1])
            
            # Check if any prediction is restricted
            is_restricted = any(pred.get('is_restricted', False) for pred in predictions)
            
            return {
                'category': best_category[0],
                'confidence': float(best_category[1]),
                'is_restricted': is_restricted,
                'top_categories': sorted(category_scores.items(), key=lambda x: x[1], reverse=True)[:5]
            }
            
        except Exception as e:
            logger.error(f"Error in weighted fusion: {e}")
            return {'category': 'unknown', 'confidence': 0.0, 'error': str(e)}