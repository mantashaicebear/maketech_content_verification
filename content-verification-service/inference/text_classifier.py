"""
Text Classifier for Content Verification
Uses NLP to classify text content into categories
"""

import os
import json
import pickle
import logging
import numpy as np
from typing import Dict, List, Tuple, Any
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

from data.text_preprocessor import TextPreprocessor
from data.text_vectorizer import TextVectorizer

logger = logging.getLogger(__name__)

class TextClassifier:
    """
    Text classification using TF-IDF and Random Forest
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize text classifier
        
        Args:
            model_path: Path to saved model
        """
        self.model_path = model_path or "content-verification-service/data/outputs/"
        self.categories = [
            'food', 'tech', 'education', 'healthcare', 'finance',
            'fashion', 'electronics', 'automotive', 'real_estate',
            'entertainment', 'sports', 'travel', 'beauty', 'home',
            'weapons', 'drugs', 'adult_content', 'gambling',
            'counterfeit', 'harmful_chemicals', 'surveillance'
        ]
        
        # Initialize components
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TextVectorizer()
        
        # Load or train model
        self.model = self._load_model()
        
        logger.info(f"TextClassifier initialized with {len(self.categories)} categories")
    
    def _load_model(self):
        """Load or create model"""
        model_file = os.path.join(self.model_path, "text_classifier.pkl")
        vectorizer_file = os.path.join(self.model_path, "tfidf_vectorizer.pkl")
        
        try:
            if os.path.exists(model_file) and os.path.exists(vectorizer_file):
                # Load existing model
                self.vectorizer = joblib.load(vectorizer_file)
                model = joblib.load(model_file)
                logger.info("Loaded existing text classification model")
                return model
            else:
                # Create new model
                logger.info("Creating new text classification model")
                return self._create_model()
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return self._create_model()
    
    def _create_model(self):
        """Create a new model"""
        # This would typically train on your dataset
        # For now, create a simple model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42
        )
        
        # Train on dummy data (replace with actual training)
        self._train_dummy_model(model)
        
        return model
    
    def _train_dummy_model(self, model):
        """Train model on dummy data"""
        # Generate dummy training data
        texts = []
        labels = []
        
        # Create training examples for each category
        category_keywords = {
            'food': ['recipe', 'cooking', 'restaurant', 'meal', 'food'],
            'tech': ['software', 'coding', 'computer', 'technology', 'app'],
            'education': ['learning', 'course', 'study', 'education', 'school'],
            'weapons': ['gun', 'rifle', 'pistol', 'weapon', 'firearm'],
            'drugs': ['drug', 'cocaine', 'heroin', 'marijuana', 'narcotic'],
            'adult_content': ['adult', 'porn', 'xxx', 'explicit', 'nsfw'],
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                texts.append(f"This is about {keyword} and related things")
                labels.append(category)
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(texts)
        y = np.array([self.categories.index(label) if label in self.categories else 0 for label in labels])
        
        # Train model
        model.fit(X, y)
        
        # Save model
        model_file = os.path.join(self.model_path, "text_classifier.pkl")
        vectorizer_file = os.path.join(self.model_path, "tfidf_vectorizer.pkl")
        
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(model, model_file)
        joblib.dump(self.vectorizer, vectorizer_file)
        
        logger.info(f"Model trained and saved to {model_file}")
    
    def predict(self, text: str) -> Dict:
        """
        Predict category for text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with prediction results
        """
        try:
            if not text or not text.strip():
                return {
                    "category": "unknown",
                    "confidence": 0.0,
                    "is_restricted": False,
                    "error": "Empty text"
                }
            
            # Preprocess text
            processed_text = self.preprocessor.preprocess(text)
            
            # Vectorize
            X = self.vectorizer.transform([processed_text])
            
            # Predict
            probabilities = self.model.predict_proba(X)[0]
            predicted_idx = np.argmax(probabilities)
            confidence = probabilities[predicted_idx]
            
            # Get top categories
            top_indices = np.argsort(probabilities)[-5:][::-1]
            top_categories = [
                (self.categories[idx], float(probabilities[idx]))
                for idx in top_indices
            ]
            
            predicted_category = self.categories[predicted_idx]
            
            # Check if restricted
            is_restricted = predicted_category in [
                'weapons', 'drugs', 'adult_content', 'gambling',
                'counterfeit', 'harmful_chemicals', 'surveillance'
            ]
            
            # Extract keywords
            keywords = self._extract_keywords(text)
            
            result = {
                "category": predicted_category,
                "confidence": float(confidence),
                "is_restricted": is_restricted,
                "top_categories": top_categories,
                "keywords": keywords,
                "text_length": len(text),
                "processed_text": processed_text[:100] + "..." if len(processed_text) > 100 else processed_text
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in text prediction: {e}")
            return {
                "category": "unknown",
                "confidence": 0.0,
                "is_restricted": False,
                "error": str(e)
            }
    
    def _extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract important keywords from text"""
        try:
            # Simple keyword extraction
            words = re.findall(r'\b\w+\b', text.lower())
            word_freq = {}
            
            for word in words:
                if len(word) > 3:  # Ignore short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            
            return [word for word, freq in sorted_words[:top_n]]
            
        except:
            return []
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return self.categories
    
    def batch_predict(self, texts: List[str]) -> List[Dict]:
        """
        Predict categories for multiple texts
        
        Args:
            texts: List of texts
            
        Returns:
            List of prediction results
        """
        results = []
        for text in texts:
            result = self.predict(text)
            results.append(result)
        return results
    
    def save_model(self, path: str = None):
        """Save model to disk"""
        try:
            path = path or self.model_path
            os.makedirs(path, exist_ok=True)
            
            model_file = os.path.join(path, "text_classifier.pkl")
            vectorizer_file = os.path.join(path, "tfidf_vectorizer.pkl")
            
            joblib.dump(self.model, model_file)
            joblib.dump(self.vectorizer, vectorizer_file)
            
            logger.info(f"Model saved to {path}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")