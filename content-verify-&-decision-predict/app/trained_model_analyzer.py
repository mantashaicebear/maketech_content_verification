"""
Trained Model-Based Content Analyzer
Uses trained ML models instead of Gemini API
"""

import os
import sys
import json
import pickle
import numpy as np
import logging
from typing import Dict

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from data.text_preprocessor import TextPreprocessor

logger = logging.getLogger(__name__)

class TrainedModelAnalyzer:
    """Analyze content using trained models"""
    
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models", "trained")
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
        self.text_preprocessor = TextPreprocessor()
        
        # Load models
        self.category_model = self._load_model("category_classifier.pkl")
        self.decision_model = self._load_model("decision_classifier.pkl")
        self.text_vectorizer = self._load_model("text_vectorizer.pkl")
        self.category_mapping = self._load_json("category_mapping.json")
        
        # Load business profiles
        self.business_profiles = self._load_business_profiles()
        
        logger.info("TrainedModelAnalyzer initialized successfully")
    
    def _load_model(self, filename: str):
        """Load pickle model"""
        path = os.path.join(self.models_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model not found: {path}. Please run train_models.py first.")
        
        with open(path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Loaded model: {filename}")
        return model
    
    def _load_json(self, filename: str):
        """Load JSON file"""
        path = os.path.join(self.models_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"JSON file not found: {path}")
        
        with open(path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded JSON: {filename}")
        return data
    
    def _load_business_profiles(self):
        """Load business profiles from data directory"""
        path = os.path.join(self.data_dir, "business_profiles.json")
        if not os.path.exists(path):
            logger.warning(f"Business profiles not found: {path}")
            return {}
        
        with open(path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} business profiles")
        return data
    
    def analyze_content(self, user_text: str, registered_domain: str, business_id: str = None) -> Dict:
        """
        Analyze content using trained models
        
        Args:
            user_text: The content to analyze
            registered_domain: The business's registered domain
            business_id: Optional business ID to check multi-domain allowance
        
        Returns:
            Analysis result with status, reason, confidence, detected_category
        """
        try:
            # Preprocess text
            processed_text = self.text_preprocessor.preprocess(user_text)
            
            if not processed_text or processed_text.strip() == "":
                # If text is empty after preprocessing
                return {
                    "status": "Flagged for Manual Review",
                    "reason": "Text is too short or contains no meaningful content.",
                    "confidence_score": 0.0,
                    "detected_category": "other"
                }
            
            # Vectorize text - handle single string
            X = self.text_vectorizer.transform([processed_text])
            
            # Ensure we have the right shape
            if X.shape[0] != 1:
                X = X.reshape(1, -1)
            
            # Predict category
            category_pred = self.category_model.predict(X)[0]
            category_proba = self.category_model.predict_proba(X)[0]
            category_confidence = float(np.max(category_proba))
            
            # Map category ID to name
            detected_category = self.category_mapping.get(str(int(category_pred)), "unknown")
            
            # Log for debugging
            logger.debug(f"Category prediction: {category_pred} -> {detected_category}")
            logger.debug(f"Category confidence: {category_confidence:.2%}")
            
            # Predict decision (allowed/not allowed)
            decision_pred = self.decision_model.predict(X)[0]
            decision_proba = self.decision_model.predict_proba(X)[0]
            decision_confidence = float(np.max(decision_proba))
            
            # Log for debugging
            logger.debug(f"Decision prediction: {decision_pred} (0=blocked, 1=allowed)")
            logger.debug(f"Decision confidence: {decision_confidence:.2%}")
            
            # Check domain alignment
            domain_match = detected_category.lower() == registered_domain.lower()
            
            # Check if business is allowed to post in detected category (multi-domain support)
            is_allowed_in_business_domains = False
            business_allowed_domains = []
            is_registered_domain_valid = False
            
            if business_id and business_id in self.business_profiles:
                business_info = self.business_profiles[business_id]
                business_allowed_domains = business_info.get('domains', [registered_domain])
                # For a post to be approved:
                # 1. registered_domain must be in business's allowed domains
                # 2. detected_category must match registered_domain
                is_registered_domain_valid = registered_domain.lower() in [d.lower() for d in business_allowed_domains]
                is_allowed_in_business_domains = domain_match and is_registered_domain_valid
                logger.debug(f"Business {business_id} allowed domains: {business_allowed_domains}")
                logger.debug(f"Registered domain '{registered_domain}' valid for business: {is_registered_domain_valid}")
                logger.debug(f"Detected category matches registered domain: {domain_match}")
                logger.debug(f"Is allowed in business domains: {is_allowed_in_business_domains}")
            else:
                # If no business_id provided, fall back to registered_domain check
                is_allowed_in_business_domains = domain_match
                is_registered_domain_valid = True
                business_allowed_domains = [registered_domain]
            
            # Restricted categories (should always be blocked)
            restricted_categories = ['weapons', 'drugs', 'adult_content', 'gambling']
            
            # Determine status - Business domain check takes priority over decision model
            if detected_category == "unknown":
                status = "Flagged for Manual Review"
                reason = "Unable to determine content category."
                confidence_score = category_confidence
            elif detected_category in restricted_categories:
                # Restricted content is ALWAYS blocked regardless of business or confidence
                # Even with low confidence, we reject restricted categories for safety
                status = "Rejected: Restricted Content"
                reason = f"Content classified as '{detected_category}' which is restricted for all businesses."
                confidence_score = category_confidence
            elif business_id and not is_registered_domain_valid:
                # Registered domain is not valid for this business
                status = "Rejected: Invalid Registered Domain"
                reason = f"Registered domain '{registered_domain}' is not allowed for business '{business_id}'. Allowed domains: {', '.join(business_allowed_domains)}."
                confidence_score = category_confidence
            elif is_allowed_in_business_domains:
                # Business IS allowed to post in this category
                # But check confidence threshold for non-restricted content
                if category_confidence < 0.15:  # Lowered from 0.20 to 0.15 (15% threshold)
                    status = "Flagged for Manual Review"
                    if business_id:
                        reason = f"Content detected as '{detected_category}' (allowed for business '{business_id}'), but confidence is very low ({category_confidence:.2%})."
                    else:
                        reason = f"Content matches domain '{registered_domain}', but confidence is very low ({category_confidence:.2%})."
                    confidence_score = category_confidence
                else:
                    status = "Approved"
                    if business_id:
                        reason = f"Content matches allowed domain '{detected_category}' for business '{business_id}'."
                    else:
                        reason = f"Content matches domain '{registered_domain}'."
                    confidence_score = category_confidence
            elif not is_allowed_in_business_domains:
                # Business is NOT allowed to post in this category (domain mismatch)
                status = "Rejected: Domain Mismatch"
                if business_id:
                    reason = f"Content detected as '{detected_category}' but business '{business_id}' is only allowed to post in: {', '.join(business_allowed_domains)}."
                else:
                    reason = f"Content detected as '{detected_category}' but business registered for '{registered_domain}'."
                confidence_score = category_confidence
            else:
                # Fallback (shouldn't reach here)
                status = "Flagged for Manual Review"
                reason = "Unable to determine content allowance."
                confidence_score = category_confidence
            
            return {
                "status": status,
                "reason": reason,
                "confidence": round(confidence_score, 4),
                "confidence_score": round(confidence_score, 4),
                "predicted_category": detected_category,
                "detected_category": detected_category,
                "domain_match": domain_match,
                "is_allowed_in_business_domains": is_allowed_in_business_domains,
                "business_allowed_domains": business_allowed_domains,
                "category_confidence": round(category_confidence, 4),
                "decision_confidence": round(decision_confidence, 4)
            }
        
        except Exception as e:
            logger.error(f"Error analyzing content: {e}", exc_info=True)
            return {
                "status": "Error",
                "reason": f"An error occurred during analysis: {str(e)}",
                "confidence_score": 0.0,
                "detected_category": "error",
                "error": str(e)
            }


def analyze_content(user_text: str, registered_domain: str, business_id: str = None) -> dict:
    """
    Main function to analyze content using trained models
    This replaces the Gemini API call
    """
    try:
        analyzer = TrainedModelAnalyzer()
        result = analyzer.analyze_content(user_text, registered_domain, business_id)
        return result
    except FileNotFoundError as e:
        logger.error(f"Models not trained yet: {e}")
        return {
            "status": "Error",
            "reason": "Models not trained yet. Please run: python train_models.py",
            "confidence_score": 0.0,
            "detected_category": "error",
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Error in analyze_content: {e}")
        return {
            "status": "Error",
            "reason": f"An error occurred: {str(e)}",
            "confidence_score": 0.0,
            "detected_category": "error",
            "error": str(e)
        }
