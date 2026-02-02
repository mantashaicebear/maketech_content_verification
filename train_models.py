"""
Model Training Script
Trains text and image classifiers using the generated dataset
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import logging

from data.dataset_generator import DatasetGenerator
from data.text_preprocessor import TextPreprocessor
from data.text_vectorizer import TextVectorizer
from inference.text_classifier import TextClassifier
from database.business_profiles import BusinessProfileDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Train ML models for content verification"""
    
    def __init__(self):
        self.dataset_generator = DatasetGenerator()
        self.text_preprocessor = TextPreprocessor()
        # Optimized vectorizer parameters for maximum accuracy
        self.text_vectorizer = TextVectorizer(
            max_features=2000,      # Increased from 1000 for even richer features
            ngram_range=(1, 3)      # Include trigrams for better context
        )
        self.models_dir = "models/trained"
        self.data_dir = "data"
        
        # Create models directory if not exists
        os.makedirs(self.models_dir, exist_ok=True)
    
    def load_or_generate_dataset(self, csv_path: str = None) -> pd.DataFrame:
        """Load dataset from CSV or generate new one"""
        if csv_path and os.path.exists(csv_path):
            logger.info(f"Loading dataset from {csv_path}")
            df = pd.read_csv(csv_path)
        else:
            logger.info("Generating new dataset...")
            df = self.dataset_generator.generate_dataset_with_business_ids(samples_per_category=50)
            csv_path = os.path.join(self.data_dir, "content_verification_dataset.csv")
            df.to_csv(csv_path, index=False)
            logger.info(f"Dataset saved to {csv_path}")
        
        logger.info(f"Dataset shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        return df
    
    def prepare_text_data(self, df: pd.DataFrame):
        """Prepare text data for training"""
        logger.info("Preparing text data...")
        
        # Preprocess texts
        texts = df['text'].apply(self.text_preprocessor.preprocess).tolist()
        
        # Vectorize texts
        X = self.text_vectorizer.fit_transform(texts)
        
        # Prepare labels
        categories = df['category'].tolist()
        category_to_id = {cat: idx for idx, cat in enumerate(sorted(set(categories)))}
        y = np.array([category_to_id[cat] for cat in categories])
        
        logger.info(f"Text data shape: X={X.shape}, y={y.shape}")
        logger.info(f"Categories: {category_to_id}")
        
        return X, y, texts, category_to_id
    
    def prepare_decision_data(self, df: pd.DataFrame):
        """Prepare data for decision engine (domain alignment)"""
        logger.info("Preparing decision data...")
        
        # Preprocess texts
        texts = df['text'].apply(self.text_preprocessor.preprocess).tolist()
        
        # Vectorize texts
        X = self.text_vectorizer.fit_transform(texts)
        
        # Prepare labels (0 = not allowed, 1 = allowed)
        y = df['is_allowed'].values
        
        logger.info(f"Decision data shape: X={X.shape}, y={y.shape}")
        logger.info(f"Allowed: {sum(y)} / Not Allowed: {sum(1-y)}")
        
        return X, y, texts
    
    def train_category_classifier(self, X, y, category_to_id):
        """Train category classification model with optimized hyperparameters"""
        logger.info("Training category classifier...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest with highly optimized hyperparameters for maximum accuracy
        model = RandomForestClassifier(
            n_estimators=300,          # Increased from 200 for better ensemble
            max_depth=40,              # Increased from 30 for deeper patterns
            min_samples_split=2,       # Fine-tuning
            min_samples_leaf=1,        # Fine-tuning
            max_features='sqrt',       # Better generalization
            bootstrap=True,
            class_weight='balanced',   # Handle imbalanced classes
            criterion='gini',          # Split criterion
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        logger.info(f"Category Classifier - Train Accuracy: {train_score:.4f}, Test Accuracy: {test_score:.4f}")
        
        # Save model
        model_path = os.path.join(self.models_dir, "category_classifier.pkl")
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Category classifier saved to {model_path}")
        
        # Save category mapping
        mapping_path = os.path.join(self.models_dir, "category_mapping.json")
        id_to_category = {str(v): k for k, v in category_to_id.items()}
        with open(mapping_path, 'w') as f:
            json.dump(id_to_category, f, indent=2)
        logger.info(f"Category mapping saved to {mapping_path}")
        
        return model, category_to_id
    
    def train_decision_classifier(self, X, y):
        """Train decision classifier with optimized hyperparameters"""
        logger.info("Training decision classifier...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Logistic Regression with optimized hyperparameters
        model = LogisticRegression(
            C=10.0,                    # Regularization strength (inverse)
            penalty='l2',              # L2 regularization
            solver='lbfgs',            # Optimization algorithm
            max_iter=2000,             # Increased from 1000
            class_weight='balanced',   # Handle imbalanced classes
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        logger.info(f"Decision Classifier - Train Accuracy: {train_score:.4f}, Test Accuracy: {test_score:.4f}")
        
        # Save model
        model_path = os.path.join(self.models_dir, "decision_classifier.pkl")
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Decision classifier saved to {model_path}")
        
        return model
    
    def save_vectorizer(self):
        """Save the fitted vectorizer"""
        vectorizer_path = os.path.join(self.models_dir, "text_vectorizer.pkl")
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.text_vectorizer, f)
        logger.info(f"Text vectorizer saved to {vectorizer_path}")
    
    def train(self, dataset_path: str = None):
        """Complete training pipeline"""
        logger.info("=" * 60)
        logger.info("Starting Model Training")
        logger.info("=" * 60)
        
        # Load or generate dataset
        df = self.load_or_generate_dataset(dataset_path)
        
        # Train category classifier
        X_cat, y_cat, texts_cat, category_to_id = self.prepare_text_data(df)
        category_model = self.train_category_classifier(X_cat, y_cat, category_to_id)
        
        # Train decision classifier
        X_dec, y_dec, texts_dec = self.prepare_decision_data(df)
        decision_model = self.train_decision_classifier(X_dec, y_dec)
        
        # Save vectorizer
        self.save_vectorizer()
        
        logger.info("=" * 60)
        logger.info("Training Complete!")
        logger.info("=" * 60)
        logger.info(f"Models saved to: {self.models_dir}")
        logger.info(f"Category Classifier: {os.path.join(self.models_dir, 'category_classifier.pkl')}")
        logger.info(f"Decision Classifier: {os.path.join(self.models_dir, 'decision_classifier.pkl')}")
        logger.info(f"Text Vectorizer: {os.path.join(self.models_dir, 'text_vectorizer.pkl')}")
        logger.info(f"Category Mapping: {os.path.join(self.models_dir, 'category_mapping.json')}")
        
        return category_model, decision_model

if __name__ == "__main__":
    trainer = ModelTrainer()
    
    # Train models using existing dataset
    dataset_path = os.path.join("data", "content_verification_dataset.csv")
    trainer.train(dataset_path)
