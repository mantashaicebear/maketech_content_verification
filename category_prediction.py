"""
Main Category Prediction Module
Handles both text and image content classification
"""

import os
import sys
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms

# Add the service directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'content-verification-service'))

from api.verify_content import ContentVerificationAPI
from inference.text_classifier import TextClassifier
from inference.image_classifier import ImageClassifier
from inference.fusion import FusionClassifier
from policy.decision_engine import DecisionEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CategoryPredictor:
    """
    Main class for predicting categories of content (text + images)
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the category predictor
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        
        # Initialize classifiers
        logger.info("Initializing text classifier...")
        self.text_classifier = TextClassifier()
        
        logger.info("Initializing image classifier...")
        self.image_classifier = ImageClassifier()
        
        logger.info("Initializing fusion classifier...")
        self.fusion_classifier = FusionClassifier(
            text_classifier=self.text_classifier,
            image_classifier=self.image_classifier
        )
        
        logger.info("Initializing decision engine...")
        self.decision_engine = DecisionEngine()
        
        logger.info("CategoryPredictor initialized successfully")
    
    def _load_config(self, config_path: str = None) -> Dict:
        """Load configuration from file or use defaults"""
        default_config = {
            'threshold': 0.5,
            'restricted_categories': [
                'weapons', 'drugs', 'explosives', 'prescription_medicine',
                'alcohol', 'tobacco', 'counterfeit', 'human_organs',
                'wildlife', 'harmful_chemicals', 'surveillance',
                'hacking_tools', 'gambling', 'adult_content',
                'hate_speech', 'pyramid_schemes'
            ],
            'business_domains': [
                'food', 'tech', 'education', 'healthcare', 'finance',
                'fashion', 'electronics', 'automotive', 'real_estate',
                'entertainment', 'sports', 'travel', 'beauty', 'home'
            ],
            'fusion_weights': {
                'text': 0.6,
                'image': 0.4
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                default_config.update(config)
                logger.info(f"Configuration loaded from {config_path}")
            except Exception as e:
                logger.error(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def predict_text(self, text: str, title: str = "") -> Dict:
        """
        Predict category for text content
        
        Args:
            text: Main content text
            title: Optional title
            
        Returns:
            Dictionary with prediction results
        """
        try:
            logger.info(f"Predicting category for text: {title[:50]}...")
            
            # Combine title and text for better prediction
            combined_text = f"{title} {text}" if title else text
            
            # Get prediction from text classifier
            text_prediction = self.text_classifier.predict(combined_text)
            
            # Check against restricted categories
            is_restricted = text_prediction['category'] in self.config['restricted_categories']
            
            result = {
                'content_type': 'text',
                'predicted_category': text_prediction['category'],
                'confidence': float(text_prediction['confidence']),
                'is_restricted': is_restricted,
                'top_categories': text_prediction.get('top_categories', []),
                'features': text_prediction.get('features', {}),
                'model_used': 'text_classifier'
            }
            
            logger.info(f"Text prediction: {text_prediction['category']} "
                       f"(confidence: {text_prediction['confidence']:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in text prediction: {e}")
            return {
                'content_type': 'text',
                'predicted_category': 'unknown',
                'confidence': 0.0,
                'is_restricted': False,
                'error': str(e)
            }
    
    def predict_image(self, image_path: str) -> Dict:
        """
        Predict category for image content
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with prediction results
        """
        try:
            logger.info(f"Predicting category for image: {image_path}")
            
            # Check if image exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            
            # Get prediction from image classifier
            image_prediction = self.image_classifier.predict(image)
            
            # Check against restricted categories
            is_restricted = image_prediction['category'] in self.config['restricted_categories']
            
            result = {
                'content_type': 'image',
                'predicted_category': image_prediction['category'],
                'confidence': float(image_prediction['confidence']),
                'is_restricted': is_restricted,
                'top_categories': image_prediction.get('top_categories', []),
                'features': image_prediction.get('features', {}),
                'model_used': 'image_classifier'
            }
            
            logger.info(f"Image prediction: {image_prediction['category']} "
                       f"(confidence: {image_prediction['confidence']:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in image prediction: {e}")
            return {
                'content_type': 'image',
                'predicted_category': 'unknown',
                'confidence': 0.0,
                'is_restricted': False,
                'error': str(e)
            }
    
    def predict_mixed(self, text: str, image_paths: List[str], title: str = "") -> Dict:
        """
        Predict category for mixed content (text + images)
        
        Args:
            text: Main content text
            image_paths: List of image file paths
            title: Optional title
            
        Returns:
            Dictionary with prediction results
        """
        try:
            logger.info(f"Predicting category for mixed content with {len(image_paths)} images")
            
            # Get text prediction
            text_result = self.predict_text(text, title) if text else None
            
            # Get image predictions
            image_results = []
            for img_path in image_paths:
                if os.path.exists(img_path):
                    img_result = self.predict_image(img_path)
                    image_results.append(img_result)
            
            # Fuse predictions if we have both text and images
            if text_result and image_results:
                # Use fusion classifier
                fusion_result = self.fusion_classifier.fuse_predictions(
                    text_prediction=text_result,
                    image_predictions=image_results,
                    weights=self.config['fusion_weights']
                )
                
                result = {
                    'content_type': 'mixed',
                    'predicted_category': fusion_result['category'],
                    'confidence': fusion_result['confidence'],
                    'is_restricted': fusion_result['is_restricted'],
                    'top_categories': fusion_result.get('top_categories', []),
                    'text_predictions': text_result,
                    'image_predictions': image_results,
                    'fusion_weights': self.config['fusion_weights'],
                    'model_used': 'fusion_classifier'
                }
                
                logger.info(f"Fusion prediction: {fusion_result['category']} "
                           f"(confidence: {fusion_result['confidence']:.2f})")
                
            elif text_result:
                # Only text
                result = text_result
                result['content_type'] = 'text_only'
                
            elif image_results:
                # Only images - take the highest confidence prediction
                best_image = max(image_results, key=lambda x: x['confidence'])
                result = best_image
                result['content_type'] = 'image_only'
                result['all_image_predictions'] = image_results
                
            else:
                # No content
                result = {
                    'content_type': 'empty',
                    'predicted_category': 'unknown',
                    'confidence': 0.0,
                    'is_restricted': False
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in mixed content prediction: {e}")
            return {
                'content_type': 'mixed',
                'predicted_category': 'unknown',
                'confidence': 0.0,
                'is_restricted': False,
                'error': str(e)
            }
    
    def verify_content_for_business(
        self,
        content: Dict[str, Any],
        business_profile: Dict[str, Any]
    ) -> Dict:
        """
        Verify content against business rules
        
        Args:
            content: Content dictionary with text and/or images
            business_profile: Business profile information
            
        Returns:
            Dictionary with verification results
        """
        try:
            logger.info(f"Verifying content for business: {business_profile.get('business_name')}")
            
            # Extract content data
            text = content.get('text', '')
            title = content.get('title', '')
            image_paths = content.get('image_paths', [])
            
            # Get prediction
            if text and image_paths:
                prediction = self.predict_mixed(text, image_paths, title)
            elif text:
                prediction = self.predict_text(text, title)
            elif image_paths:
                prediction = self.predict_image(image_paths[0])
            else:
                prediction = {
                    'predicted_category': 'unknown',
                    'confidence': 0.0,
                    'is_restricted': False
                }
            
            # Apply business decision logic
            decision = self.decision_engine.make_decision(
                content_prediction=prediction,
                business_profile=business_profile
            )
            
            # Combine prediction and decision
            result = {
                **prediction,
                'decision': decision['decision'],
                'is_allowed': decision['is_allowed'],
                'reason': decision['reason'],
                'warning_message': decision.get('warning_message', ''),
                'requires_review': decision.get('requires_review', False),
                'business_type': business_profile.get('business_type'),
                'business_domain': business_profile.get('business_domain')
            }
            
            logger.info(f"Verification result: {decision['decision']} - {decision['reason']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in content verification: {e}")
            return {
                'error': str(e),
                'decision': 'error',
                'is_allowed': False,
                'reason': f'Verification error: {str(e)}'
            }
    
    def batch_predict(self, contents: List[Dict]) -> List[Dict]:
        """
        Predict categories for multiple contents
        
        Args:
            contents: List of content dictionaries
            
        Returns:
            List of prediction results
        """
        results = []
        for content in contents:
            try:
                text = content.get('text', '')
                image_paths = content.get('image_paths', [])
                
                if text and image_paths:
                    result = self.predict_mixed(text, image_paths)
                elif text:
                    result = self.predict_text(text)
                elif image_paths:
                    result = self.predict_image(image_paths[0])
                else:
                    result = {'error': 'No content provided'}
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error in batch prediction: {e}")
                results.append({'error': str(e)})
        
        return results


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Category Prediction for Content Verification')
    parser.add_argument('--text', type=str, help='Text content to classify')
    parser.add_argument('--image', type=str, help='Image path to classify')
    parser.add_argument('--title', type=str, default='', help='Title of the content')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--batch', action='store_true', help='Process in batch mode')
    parser.add_argument('--input_file', type=str, help='Input JSON file for batch processing')
    
    args = parser.parse_args()
    
    # Initialize predictor
    predictor = CategoryPredictor(config_path=args.config)
    
    if args.batch and args.input_file:
        # Batch processing
        try:
            with open(args.input_file, 'r') as f:
                contents = json.load(f)
            
            results = predictor.batch_predict(contents)
            
            # Save results
            output_file = args.input_file.replace('.json', '_results.json')
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"Batch processing completed. Results saved to {output_file}")
            
        except Exception as e:
            print(f"Error in batch processing: {e}")
    
    elif args.text or args.image:
        # Single prediction
        if args.text and args.image:
            result = predictor.predict_mixed(args.text, [args.image], args.title)
        elif args.text:
            result = predictor.predict_text(args.text, args.title)
        elif args.image:
            result = predictor.predict_image(args.image)
        
        # Print result
        print("\n" + "="*50)
        print("CATEGORY PREDICTION RESULT")
        print("="*50)
        print(f"Content Type: {result.get('content_type', 'unknown')}")
        print(f"Predicted Category: {result.get('predicted_category', 'unknown')}")
        print(f"Confidence: {result.get('confidence', 0.0):.2%}")
        print(f"Is Restricted: {result.get('is_restricted', False)}")
        
        if 'top_categories' in result and result['top_categories']:
            print("\nTop Categories:")
            for cat, conf in result['top_categories'][:5]:
                print(f"  - {cat}: {conf:.2%}")
        
        if 'error' in result:
            print(f"\nError: {result['error']}")
        
        print("="*50)
    
    else:
        # Interactive mode
        print("Category Prediction System")
        print("1. Classify text")
        print("2. Classify image")
        print("3. Classify mixed content")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '1':
            text = input("Enter text: ")
            title = input("Enter title (optional): ")
            result = predictor.predict_text(text, title)
            
        elif choice == '2':
            image_path = input("Enter image path: ")
            result = predictor.predict_image(image_path)
            
        elif choice == '3':
            text = input("Enter text: ")
            title = input("Enter title (optional): ")
            image_paths_input = input("Enter image paths (comma-separated): ")
            image_paths = [p.strip() for p in image_paths_input.split(',') if p.strip()]
            result = predictor.predict_mixed(text, image_paths, title)
            
        else:
            print("Exiting...")
            return
        
        # Display result
        print("\nResult:")
        print(f"Category: {result.get('predicted_category', 'unknown')}")
        print(f"Confidence: {result.get('confidence', 0.0):.2%}")


if __name__ == "__main__":
    main()