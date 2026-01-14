"""Data module - Dataset creation, preprocessing, vectorization."""

from .dataset_generator import create_dummy_dataset
from .text_preprocessor import preprocess_text
from .text_vectorizer import vectorize_text

__all__ = [
    'create_dummy_dataset',
    'preprocess_text',
    'vectorize_text',
]
