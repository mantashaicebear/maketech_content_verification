"""
Image Classifier for Content Verification
"""

from PIL import Image
import numpy as np
from typing import Dict

class ImageClassifier:
    """Image classification using neural networks"""
    
    def __init__(self):
        try:
            import torchvision.transforms as transforms
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            self.torch_available = True
        except (ImportError, OSError, RuntimeError):
            self.torch_available = False
            self.transform = None
        
        self.categories = [
            'food', 'tech', 'education', 'health', 'finance', 'fashion',
            'electronics', 'automotive', 'real_estate', 'entertainment',
            'weapons', 'drugs', 'adult_content', 'gambling', 'document',
            'person', 'nature', 'vehicle', 'other'
        ]
        
        self.restricted_categories = ['weapons', 'drugs', 'adult_content', 'gambling']
    
    def predict(self, image: Image.Image) -> Dict:
        """Predict category for image"""
        try:
            # Transform image
            input_tensor = self.transform(image).unsqueeze(0)
            
            # Mock prediction (in real implementation, use trained model)
            # For now, return random predictions
            np.random.seed(hash(str(image.size)) % 10000)
            probabilities = np.random.rand(len(self.categories))
            probabilities = probabilities / probabilities.sum()
            
            predicted_idx = np.argmax(probabilities)
            confidence = probabilities[predicted_idx]
            
            predicted_category = self.categories[predicted_idx]
            
            # Get top categories
            top_indices = np.argsort(probabilities)[-3:][::-1]
            top_categories = [
                (self.categories[idx], float(probabilities[idx]))
                for idx in top_indices
            ]
            
            # Check if restricted
            is_restricted = predicted_category in self.restricted_categories
            
            return {
                'category': predicted_category,
                'confidence': float(confidence),
                'is_restricted': is_restricted,
                'top_categories': top_categories,
                'image_size': image.size
            }
            
        except Exception as e:
            return {
                'category': 'error',
                'confidence': 0.0,
                'is_restricted': False,
                'error': str(e)
            }
    
    def predict_from_path(self, image_path: str) -> Dict:
        """Predict category from image file path"""
        try:
            image = Image.open(image_path).convert('RGB')
            result = self.predict(image)
            result['image_path'] = image_path
            return result
        except Exception as e:
            return {
                'category': 'error',
                'confidence': 0.0,
                'is_restricted': False,
                'error': str(e)
            }