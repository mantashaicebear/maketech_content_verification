"""
Content Verification API
Handles API requests for content verification
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from inference.text_classifier import TextClassifier
from inference.image_classifier import ImageClassifier
from inference.fusion import FusionClassifier
from policy.decision_engine import DecisionEngine
from database.business_profiles import BusinessProfileDB

# Configure logging
logger = logging.getLogger(__name__)

class ContentVerificationAPI:
    """
    Main API class for content verification
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the API
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        
        # Initialize classifiers
        logger.info("Initializing classifiers...")
        self.text_classifier = TextClassifier()
        self.image_classifier = ImageClassifier()
        self.fusion_classifier = FusionClassifier(
            text_classifier=self.text_classifier,
            image_classifier=self.image_classifier
        )
        
        # Initialize decision engine
        self.decision_engine = DecisionEngine()
        
        # Initialize database
        self.business_db = BusinessProfileDB()
        
        logger.info("ContentVerificationAPI initialized successfully")
    
    def _load_config(self, config_path: str = None) -> Dict:
        """Load configuration"""
        default_config = {
            "restricted_categories_file": "policy/restricted_categories.json",
            "business_domains": [
                "food", "tech", "education", "healthcare", "finance",
                "fashion", "electronics", "automotive", "real_estate",
                "entertainment", "sports", "travel", "beauty", "home"
            ],
            "fusion_weights": {
                "text": 0.6,
                "image": 0.4
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                default_config.update(config)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        
        return default_config
    
    def verify_text(
        self,
        text: str,
        title: str = "",
        business_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Verify text content
        
        Args:
            text: Content text
            title: Content title
            business_profile: Business profile for context
            
        Returns:
            Verification result
        """
        try:
            # Get text prediction
            text_result = self.text_classifier.predict(f"{title} {text}")
            
            # Make decision if business profile is provided
            decision = None
            if business_profile:
                decision = self.decision_engine.make_decision(
                    content_prediction=text_result,
                    business_profile=business_profile
                )
            
            result = {
                "content_type": "text",
                "prediction": text_result,
                "decision": decision,
                "timestamp": datetime.now().isoformat(),
                "business_context": business_profile is not None
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in text verification: {e}")
            return {
                "error": str(e),
                "content_type": "text",
                "timestamp": datetime.now().isoformat()
            }
    
    def verify_image(
        self,
        image_path: str,
        business_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Verify image content
        
        Args:
            image_path: Path to image file
            business_profile: Business profile for context
            
        Returns:
            Verification result
        """
        try:
            # Get image prediction
            image_result = self.image_classifier.predict_from_path(image_path)
            
            # Make decision if business profile is provided
            decision = None
            if business_profile:
                decision = self.decision_engine.make_decision(
                    content_prediction=image_result,
                    business_profile=business_profile
                )
            
            result = {
                "content_type": "image",
                "prediction": image_result,
                "decision": decision,
                "timestamp": datetime.now().isoformat(),
                "business_context": business_profile is not None
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in image verification: {e}")
            return {
                "error": str(e),
                "content_type": "image",
                "timestamp": datetime.now().isoformat()
            }
    
    def verify_mixed(
        self,
        text: str,
        title: str = "",
        image_paths: List[str] = None,
        business_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Verify mixed content (text + images)
        
        Args:
            text: Content text
            title: Content title
            image_paths: List of image paths
            business_profile: Business profile for context
            
        Returns:
            Verification result
        """
        try:
            image_paths = image_paths or []
            
            # Get text prediction
            text_result = None
            if text or title:
                text_result = self.text_classifier.predict(f"{title} {text}")
            
            # Get image predictions
            image_results = []
            for img_path in image_paths:
                if os.path.exists(img_path):
                    img_result = self.image_classifier.predict_from_path(img_path)
                    image_results.append(img_result)
            
            # Fuse predictions
            if text_result and image_results:
                prediction = self.fusion_classifier.fuse_predictions(
                    text_prediction=text_result,
                    image_predictions=image_results,
                    weights=self.config["fusion_weights"]
                )
                prediction["source_predictions"] = {
                    "text": text_result,
                    "images": image_results
                }
            elif text_result:
                prediction = text_result
                prediction["source"] = "text_only"
            elif image_results:
                # Use highest confidence image prediction
                prediction = max(image_results, key=lambda x: x.get("confidence", 0))
                prediction["source"] = "image_only"
                prediction["all_image_predictions"] = image_results
            else:
                prediction = {
                    "category": "unknown",
                    "confidence": 0.0,
                    "is_restricted": False
                }
            
            # Make decision if business profile is provided
            decision = None
            if business_profile:
                decision = self.decision_engine.make_decision(
                    content_prediction=prediction,
                    business_profile=business_profile
                )
            
            result = {
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
            
            return result
            
        except Exception as e:
            logger.error(f"Error in mixed verification: {e}")
            return {
                "error": str(e),
                "content_type": "mixed",
                "timestamp": datetime.now().isoformat()
            }
    
    def verify_for_business(
        self,
        text: str,
        title: str = "",
        image_paths: List[str] = None,
        business_profile: Dict = None
    ) -> Dict:
        """
        Verify content for specific business
        
        Args:
            text: Content text
            title: Content title
            image_paths: List of image paths
            business_profile: Business profile
            
        Returns:
            Complete verification result
        """
        try:
            # Get content verification
            verification_result = self.verify_mixed(
                text=text,
                title=title,
                image_paths=image_paths,
                business_profile=business_profile
            )
            
            # Add business-specific information
            if business_profile:
                verification_result["business_info"] = {
                    "business_id": business_profile.get("id"),
                    "business_name": business_profile.get("business_name"),
                    "business_type": business_profile.get("business_type"),
                    "business_domain": business_profile.get("business_domain"),
                    "allowed_domains": business_profile.get("allowed_domains", [])
                }
            
            return verification_result
            
        except Exception as e:
            logger.error(f"Error in business verification: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_categories(self) -> Dict:
        """Get all available categories"""
        try:
            # Get categories from text classifier
            text_categories = self.text_classifier.get_categories()
            
            # Get categories from image classifier
            image_categories = self.image_classifier.get_categories()
            
            # Combine and deduplicate
            all_categories = list(set(text_categories + image_categories))
            
            return {
                "text_categories": text_categories,
                "image_categories": image_categories,
                "all_categories": sorted(all_categories),
                "total_categories": len(all_categories)
            }
            
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
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
            logger.error(f"Error getting restricted categories: {e}")
            return {"error": str(e)}
    
    def batch_verify(self, requests: List[Dict]) -> List[Dict]:
        """
        Batch verify multiple content requests
        
        Args:
            requests: List of verification requests
            
        Returns:
            List of verification results
        """
        results = []
        for req in requests:
            try:
                text = req.get("text", "")
                title = req.get("title", "")
                image_paths = req.get("image_paths", [])
                business_id = req.get("business_id")
                
                business_profile = None
                if business_id:
                    business_profile = self.business_db.get_profile(business_id)
                
                result = self.verify_mixed(
                    text=text,
                    title=title,
                    image_paths=image_paths,
                    business_profile=business_profile
                )
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error in batch verification: {e}")
                results.append({"error": str(e)})
        
        return results