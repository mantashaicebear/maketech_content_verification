"""
Content Verification API
"""

import os
from typing import Dict, List, Optional
from datetime import datetime

from inference.text_classifier import TextClassifier
from inference.image_classifier import ImageClassifier
from inference.fusion import FusionClassifier
from policy.decision_engine import DecisionEngine
from database.business_profiles import BusinessProfileDB

class ContentVerificationAPI:
    """Main API class for content verification"""
    
    def __init__(self):
        self.text_classifier = TextClassifier()
        self.image_classifier = ImageClassifier()
        self.fusion_classifier = FusionClassifier()
        self.decision_engine = DecisionEngine()
        self.business_db = BusinessProfileDB()
    
    def verify_text(self, text: str, title: str = "", business_profile: Optional[Dict] = None) -> Dict:
        """Verify text content"""
        try:
            # Combine title and text
            full_text = f"{title} {text}" if title else text
            
            # Get prediction
            prediction = self.text_classifier.predict(full_text)
            
            # Make decision
            decision = self.decision_engine.make_decision(prediction, business_profile)
            
            return {
                "content_type": "text",
                "prediction": prediction,
                "decision": decision,
                "timestamp": datetime.now().isoformat(),
                "business_context": business_profile is not None
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "content_type": "text",
                "timestamp": datetime.now().isoformat()
            }
    
    def verify_image(self, image_path: str, business_profile: Optional[Dict] = None) -> Dict:
        """Verify image content"""
        try:
            # Get prediction
            prediction = self.image_classifier.predict_from_path(image_path)
            
            # Make decision
            decision = self.decision_engine.make_decision(prediction, business_profile)
            
            return {
                "content_type": "image",
                "prediction": prediction,
                "decision": decision,
                "timestamp": datetime.now().isoformat(),
                "business_context": business_profile is not None
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "content_type": "image",
                "timestamp": datetime.now().isoformat()
            }
    
    def verify_mixed(self, text: str, title: str = "", image_paths: List[str] = None, 
                     business_profile: Optional[Dict] = None) -> Dict:
        """Verify mixed content (text + images)"""
        try:
            image_paths = image_paths or []
            
            # Get text prediction
            text_prediction = None
            if text or title:
                full_text = f"{title} {text}" if title else text
                text_prediction = self.text_classifier.predict(full_text)
            
            # Get image predictions
            image_predictions = []
            for img_path in image_paths:
                if os.path.exists(img_path):
                    img_pred = self.image_classifier.predict_from_path(img_path)
                    image_predictions.append(img_pred)
            
            # Fuse predictions
            if text_prediction and image_predictions:
                prediction = self.fusion_classifier.fuse_predictions(text_prediction, image_predictions)
                prediction["source"] = "fusion"
            elif text_prediction:
                prediction = text_prediction
                prediction["source"] = "text_only"
            elif image_predictions:
                # Use highest confidence image
                prediction = max(image_predictions, key=lambda x: x.get('confidence', 0))
                prediction["source"] = "image_only"
            else:
                prediction = {
                    "category": "unknown",
                    "confidence": 0.0,
                    "is_restricted": False
                }
                prediction["source"] = "none"
            
            # Make decision
            decision = self.decision_engine.make_decision(prediction, business_profile)
            
            return {
                "content_type": "mixed",
                "prediction": prediction,
                "decision": decision,
                "timestamp": datetime.now().isoformat(),
                "business_context": business_profile is not None,
                "components": {
                    "has_text": bool(text or title),
                    "has_images": bool(image_paths),
                    "image_count": len(image_paths)
                }
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "content_type": "mixed",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_categories(self) -> Dict:
        """Get available categories"""
        try:
            return {
                "text_categories": self.text_classifier.categories,
                "image_categories": self.image_classifier.categories,
                "all_categories": list(set(self.text_classifier.categories + self.image_classifier.categories))
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_restricted_categories(self) -> Dict:
        """Get restricted categories"""
        try:
            restricted = self.decision_engine.get_restricted_categories()
            return {
                "restricted_categories": restricted,
                "count": len(restricted)
            }
        except Exception as e:
            return {"error": str(e)}