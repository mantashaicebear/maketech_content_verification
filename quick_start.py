"""
Quick Start Script
Generates dataset and trains models
Run this first before starting the API server
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from train_models import ModelTrainer

def main():
    """Generate dataset and train models"""
    print("\n" + "="*70)
    print("CONTENT VERIFICATION - MODEL TRAINING")
    print("="*70 + "\n")
    
    trainer = ModelTrainer()
    
    # Check if dataset exists
    dataset_path = os.path.join("data", "content_verification_dataset.csv")
    if os.path.exists(dataset_path):
        print(f"✓ Dataset found at: {dataset_path}")
    else:
        print(f"✗ Dataset not found. Will generate new one...")
    
    # Train models
    print("\nTraining models... This may take a few moments.\n")
    category_model, decision_model = trainer.train(dataset_path)
    
    print("\n" + "="*70)
    print("✓ TRAINING COMPLETE!")
    print("="*70)
    print("\nYou can now start the API server with:")
    print("  cd content-verify-&-decision-predict")
    print("  python -m uvicorn app.main:app --reload --port 8000")
    print("\nThen visit: http://127.0.0.1:8000/docs")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
