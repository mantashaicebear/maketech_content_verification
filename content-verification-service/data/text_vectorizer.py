"""
Text Vectorization - Convert text to TF-IDF features.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def vectorize_text(texts, max_features=5000):
    """
    Convert cleaned texts to TF-IDF feature matrix.
    
    Args:
        texts: List or Series of cleaned text strings
        max_features: Maximum vocabulary size (default 5000)
    
    Returns:
        Feature matrix (sparse matrix) and feature names
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),  # Use unigrams and bigrams
        min_df=2,
        max_df=0.8
    )
    
    X = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    
    return X, feature_names, vectorizer


if __name__ == "__main__":
    # Example
    from text_preprocessor import preprocess_text
    
    texts = [
        "fresh organic coffee beans",
        "military tactical equipment",
        "python programming course"
    ]
    
    cleaned_texts = [preprocess_text(t) for t in texts]
    X, features, vectorizer = vectorize_text(cleaned_texts)
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Features: {len(features)}")
