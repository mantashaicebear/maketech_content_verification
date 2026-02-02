"""
Text Vectorizer for Content Verification - FIXED
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

class TextVectorizer:
    """Text vectorization using TF-IDF - Optimized for better accuracy"""
    
    def __init__(self, max_features: int = 1000, ngram_range: tuple = (1, 2)):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=ngram_range,  # Configurable n-gram range
            min_df=1,
            max_df=0.99,
            lowercase=True,
            sublinear_tf=True  # Apply sublinear tf scaling for better performance
        )
        self.is_fitted = False
    
    def fit(self, texts: List[str]):
        """Fit the vectorizer"""
        if not texts:
            raise ValueError("Cannot fit vectorizer with empty texts")
        
        self.vectorizer.fit(texts)
        self.is_fitted = True
        return self
    
    def transform(self, texts: List[str]) -> np.ndarray:
        """Transform texts to features"""
        if not self.is_fitted:
            # Try to fit with the provided texts
            if texts:
                self.fit(texts)
            else:
                raise ValueError("Vectorizer must be fitted first and no texts provided for fitting")
        
        # Handle single item or list
        if isinstance(texts, str):
            texts = [texts]
        
        return self.vectorizer.transform(texts).toarray()
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """Fit and transform"""
        if not texts:
            raise ValueError("Cannot fit and transform empty texts")
        
        result = self.vectorizer.fit_transform(texts).toarray()
        self.is_fitted = True
        return result
    
    def get_feature_names(self):
        """Get feature names"""
        if not self.is_fitted:
            return []
        return self.vectorizer.get_feature_names_out().tolist()