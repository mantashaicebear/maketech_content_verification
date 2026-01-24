"""
Dataset Generator for Content Verification
"""

import pandas as pd
import random
from typing import List, Dict

class DatasetGenerator:
    """Generate synthetic dataset for training"""
    
    def __init__(self):
        self.categories = {
            'food': ['food', 'restaurant', 'recipe', 'cooking', 'meal', 'dish', 'eat', 'cuisine'],
            'tech': ['software', 'coding', 'computer', 'technology', 'app', 'program', 'code', 'digital'],
            'education': ['learning', 'course', 'study', 'education', 'school', 'teach', 'learn', 'university'],
            'health': ['medical', 'health', 'doctor', 'hospital', 'medicine', 'fitness', 'wellness', 'care'],
            'finance': ['investment', 'banking', 'loan', 'finance', 'money', 'stock', 'cash', 'wealth'],
            'fashion': ['clothing', 'fashion', 'dress', 'style', 'wear', 'apparel', 'outfit', 'trend'],
            'electronics': ['electronic', 'device', 'gadget', 'phone', 'laptop', 'camera', 'smart', 'tech'],
            'automotive': ['car', 'vehicle', 'auto', 'motor', 'drive', 'engine', 'transport', 'road'],
            'real_estate': ['property', 'house', 'home', 'apartment', 'land', 'building', 'rent', 'buy'],
            'entertainment': ['movie', 'music', 'show', 'film', 'concert', 'performance', 'art', 'media'],
            'weapons': ['gun', 'rifle', 'pistol', 'weapon', 'firearm', 'ammo', 'bullet', 'combat'],
            'drugs': ['drug', 'cocaine', 'heroin', 'marijuana', 'weed', 'narcotic', 'opioid', 'pill'],
            'adult_content': ['adult', 'porn', 'xxx', 'explicit', 'nsfw', 'sexual', 'erotic', 'mature'],
            'gambling': ['casino', 'betting', 'gamble', 'lottery', 'poker', 'slot', 'bet', 'wager']
        }
    
    def generate_text(self, category: str) -> str:
        """Generate a sample text for a category"""
        keywords = self.categories.get(category, [])
        if not keywords:
            return f"This is a sample text about {category}"
        
        templates = [
            f"This is about {random.choice(keywords)} and {random.choice(keywords)}",
            f"We provide services for {random.choice(keywords)} in {category} industry",
            f"Learn more about {random.choice(keywords)} for {category} enthusiasts",
            f"Best {random.choice(keywords)} solutions for your {category} needs",
            f"Expert advice on {random.choice(keywords)} in the {category} sector"
        ]
        
        return random.choice(templates)