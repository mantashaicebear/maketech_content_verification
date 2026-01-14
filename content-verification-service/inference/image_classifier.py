"""
Image Classifier for Content Verification
Uses CNN to classify images into categories
"""

import os
import json
import logging
import numpy as np
from typing import Dict, List, Tuple, Any
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models

logger = logging.getLogger(__name__)

class ImageClassifier:
    """
    Image classification using ResNet
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize image classifier
        
        Args:
            model_path: Path to saved model
        """
        self.model_path = model_path
        self.categories = [
            'food', 'tech', 'education', 'healthcare', 'finance',
            'fashion', 'electronics', 'automotive', 'real_estate',
            'entertainment', 'sports', 'travel', 'beauty', 'home',
            'weapons', 'drugs', 'adult_content', 'gambling',
            'counterfeit', 'harmful_chemicals', 'surveillance',
            'document', 'person', 'nature', 'animal', 'vehicle'
        ]
        
        # Image transforms
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Initialize model
        self.model = self._load_model()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()
        
        logger.info(f"ImageClassifier initialized with {len(self.categories)} categories")
        logger.info(f"Using device: {self.device}")
    
    def _load_model(self):
        """Load or create model"""
        try:
            # Use pre-trained ResNet18
            model = models.resnet18(pretrained=True)
            
            # Modify final layer for our categories
            num_features = model.fc.in_features
            model.fc = nn.Linear(num_features, len(self.categories))
            
            # Load weights if available
            if self.model_path and os.path.exists(self.model_path):
                model.load_state_dict(torch.load(self.model_path, map_location='cpu'))
                logger.info(f"Loaded model from {self.model_path}")
            else:
                logger.info("Using pre-trained ResNet18 with modified classifier")
                
                # Initialize weights for new layer
                nn.init.normal_(model.fc.weight, 0, 0.01)
                nn.init.constant_(model.fc.bias, 0)
            
            return model
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def predict(self, image: Image.Image) -> Dict:
        """
        Predict category for PIL Image
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Transform image
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Predict
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
                confidence, predicted_idx = torch.max(probabilities, 0)
            
            # Get top categories
            top_conf, top_indices = torch.topk(probabilities, 5)
            top_categories = [
                (self.categories[idx.item()], conf.item())
                for conf, idx in zip(top_conf, top_indices)
            ]
            
            predicted_category = self.categories[predicted_idx.item()]
            
            # Check if restricted
            is_restricted = predicted_category in [
                'weapons', 'drugs', 'adult_content', 'gambling',
                'counterfeit', 'harmful_chemicals', 'surveillance'
            ]
            
            # Extract image features
            image_features = self._extract_features(image)
            
            result = {
                "category": predicted_category,
                "confidence": float(confidence.item()),
                "is_restricted": is_restricted,
                "top_categories": top_categories,
                "image_features": image_features,
                "image_size": image.size,
                "image_mode": image.mode
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in image prediction: {e}")
            return {
                "category": "unknown",
                "confidence": 0.0,
                "is_restricted": False,
                "error": str(e)
            }
    
    def predict_from_path(self, image_path: str) -> Dict:
        """
        Predict category for image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with prediction results
        """
        try:
            if not os.path.exists(image_path):
                return {
                    "category": "unknown",
                    "confidence": 0.0,
                    "is_restricted": False,
                    "error": f"Image not found: {image_path}"
                }
            
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Predict
            result = self.predict(image)
            result["image_path"] = image_path
            result["file_size"] = os.path.getsize(image_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Error predicting from path {image_path}: {e}")
            return {
                "category": "unknown",
                "confidence": 0.0,
                "is_restricted": False,
                "error": str(e)
            }
    
    def _extract_features(self, image: Image.Image) -> Dict:
        """Extract basic image features"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            features = {
                "height": image.height,
                "width": image.width,
                "aspect_ratio": image.width / image.height if image.height > 0 else 0,
                "channels": len(image.getbands()),
                "format": image.format or "unknown",
                "brightness": np.mean(img_array) / 255.0,
                "colorfulness": self._calculate_colorfulness(img_array)
            }
            
            return features
            
        except:
            return {}
    
    def _calculate_colorfulness(self, image: np.ndarray) -> float:
        """Calculate colorfulness metric"""
        try:
            if len(image.shape) == 3:
                # Split into RGB channels
                R, G, B = image[:,:,0], image[:,:,1], image[:,:,2]
                
                # Calculate rg and yb
                rg = np.absolute(R - G)
                yb = np.absolute(0.5 * (R + G) - B)
                
                # Calculate mean and std
                rg_mean, rg_std = np.mean(rg), np.std(rg)
                yb_mean, yb_std = np.mean(yb), np.std(yb)
                
                # Calculate colorfulness
                std_root = np.sqrt(rg_std**2 + yb_std**2)
                mean_root = np.sqrt(rg_mean**2 + yb_mean**2)
                
                return std_root + 0.3 * mean_root
            else:
                return 0.0
        except:
            return 0.0
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return self.categories
    
    def batch_predict(self, images: List[Image.Image]) -> List[Dict]:
        """
        Predict categories for multiple images
        
        Args:
            images: List of PIL Images
            
        Returns:
            List of prediction results
        """
        results = []
        for image in images:
            result = self.predict(image)
            results.append(result)
        return results
    
    def save_model(self, path: str):
        """Save model to disk"""
        try:
            torch.save(self.model.state_dict(), path)
            logger.info(f"Model saved to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")