"""
Text Vectorizer for Content Verification - FIXED
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

class TextVectorizer:
    """Text vectorization using TF-IDF - FIXED"""
    
    def __init__(self, max_features: int = 1000):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
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
        
        return self.vectorizer.transform(texts).toarray()
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """Fit and transform"""
        if not texts:
            raise ValueError("Cannot fit and transform empty texts")
        
        return self.vectorizer.fit_transform(texts).toarray()
    
    def get_feature_names(self):
        """Get feature names"""
        if not self.is_fitted:
            return []
        return self.vectorizer.get_feature_names_out().tolist()