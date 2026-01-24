"""
Complete Text Classifier for Content Verification
"""

import re
from typing import Dict, List

class TextClassifier:
    """Complete keyword-based classifier with all business domains"""
    
    def __init__(self):
        # All business domains including fashion and electronics
        self.categories = [
            'food', 'tech', 'education', 'health', 'finance', 'fashion',
            'electronics', 'automotive', 'real_estate', 'entertainment',
            'travel', 'beauty', 'home', 'sports', 'weapons', 'drugs', 
            'adult_content', 'gambling', 'other'
        ]
        
        self.restricted_categories = ['weapons', 'drugs', 'adult_content', 'gambling']
        
        # Complete keyword dictionary with all business domains
        self.keywords = {
            'tech': {
                'high': ['software', 'programming', 'coding', 'computer', 'technology', 
                        'development', 'algorithm', 'database', 'framework', 'api', 'python',
                        'javascript', 'java', 'react', 'node', 'backend', 'frontend', 'devops',
                        'mobile', 'web', 'app', 'application', 'code', 'digital'],
                'medium': ['system', 'website', 'cloud', 'cybersecurity', 'data',
                          'analysis', 'machine', 'learning', 'artificial', 'intelligence',
                          'tech', 'device', 'gadget', 'smart', 'online'],
                'low': ['internet', 'network', 'server', 'it', 'digital', 'electronic']
            },
            'food': {
                'high': ['restaurant', 'recipe', 'cooking', 'cuisine', 'culinary',
                        'menu', 'chef', 'kitchen', 'gourmet', 'dining', 'bakery',
                        'catering', 'food', 'meal', 'dish', 'eating', 'recipes'],
                'medium': ['meal', 'dish', 'food', 'eat', 'diet', 
                          'nutrition', 'ingredient', 'baking', 'grilling', 'healthy',
                          'organic', 'fresh', 'delicious', 'tasty', 'cook', 'preparation'],
                'low': ['yummy', 'flavor', 'taste', 'hungry', 'snack', 'breakfast', 'lunch', 'dinner']
            },
            'fashion': {
                'high': ['fashion', 'clothing', 'apparel', 'outfit', 'style',
                        'trend', 'designer', 'wardrobe', 'garment', 'attire',
                        'clothes', 'dress', 'shirt', 'pants', 'jacket', 'skirt'],
                'medium': ['wear', 'trendy', 'stylish', 'fashionable', 'couture',
                          'collection', 'look', 'ensemble', 'accessory', 'jewelry',
                          'shoes', 'footwear', 'bag', 'handbag', 'accessories'],
                'low': ['look', 'style', 'wear', 'dress', 'clothe', 'trend']
            },
            'electronics': {
                'high': ['electronics', 'electronic', 'device', 'gadget', 'smartphone',
                        'laptop', 'computer', 'tablet', 'camera', 'television',
                        'headphones', 'speaker', 'charger', 'battery', 'processor'],
                'medium': ['device', 'gadget', 'tech', 'smart', 'digital', 'wireless',
                          'bluetooth', 'wifi', 'screen', 'display', 'keyboard', 'mouse',
                          'printer', 'scanner', 'monitor'],
                'low': ['electronic', 'tech', 'device', 'gadget', 'smart']
            },
            'education': {
                'high': ['learning', 'course', 'education', 'teaching', 'training',
                        'university', 'college', 'school', 'academic', 'curriculum',
                        'tutorial', 'lesson', 'study', 'student', 'class', 'lecture'],
                'medium': ['study', 'student', 'lesson', 'tutorial', 'workshop',
                          'degree', 'certificate', 'online course', 'e-learning', 'learn',
                          'knowledge', 'skill', 'training', 'development', 'education'],
                'low': ['learn', 'teach', 'educate', 'knowledge', 'skill', 'study']
            },
            'health': {
                'high': ['medical', 'healthcare', 'medicine', 'hospital', 'doctor',
                        'treatment', 'therapy', 'clinic', 'pharmacy', 'wellness',
                        'fitness', 'health', 'care', 'patient', 'nurse'],
                'medium': ['fitness', 'wellbeing', 'health', 'care', 'patient',
                          'recovery', 'diagnosis', 'prevention', 'nutrition', 'exercise',
                          'workout', 'gym', 'yoga', 'meditation', 'therapy'],
                'low': ['healthy', 'fit', 'well', 'strong', 'vital', 'active']
            },
            'finance': {
                'high': ['investment', 'banking', 'finance', 'stock', 'trading',
                        'wealth', 'economy', 'market', 'portfolio', 'asset',
                        'money', 'loan', 'credit', 'bank', 'financial'],
                'medium': ['money', 'loan', 'credit', 'saving', 'budget',
                          'insurance', 'retirement', 'financial', 'capital', 'cash',
                          'profit', 'income', 'payment', 'transaction', 'banking'],
                'low': ['cash', 'rich', 'profit', 'income', 'payment', 'wealthy', 'money']
            },
            'automotive': {
                'high': ['car', 'automotive', 'vehicle', 'auto', 'automobile',
                        'motor', 'engine', 'truck', 'suv', 'sedan', 'hatchback',
                        'driving', 'road', 'transport', 'transportation'],
                'medium': ['vehicle', 'auto', 'motor', 'drive', 'road', 'highway',
                          'speed', 'mileage', 'fuel', 'gasoline', 'diesel', 'electric'],
                'low': ['car', 'drive', 'road', 'vehicle', 'auto']
            },
            'real_estate': {
                'high': ['real estate', 'property', 'house', 'home', 'apartment',
                        'land', 'building', 'rent', 'buy', 'sell', 'mortgage',
                        'property', 'realty', 'housing', 'residential', 'commercial'],
                'medium': ['house', 'home', 'apartment', 'flat', 'condo', 'villa',
                          'property', 'land', 'plot', 'construction', 'architecture'],
                'low': ['home', 'house', 'property', 'rent', 'buy']
            },
            'entertainment': {
                'high': ['entertainment', 'movie', 'music', 'show', 'film',
                        'concert', 'performance', 'art', 'media', 'television',
                        'cinema', 'theater', 'drama', 'comedy', 'action'],
                'medium': ['movie', 'music', 'show', 'film', 'song', 'album',
                          'actor', 'actress', 'director', 'producer', 'entertain'],
                'low': ['fun', 'enjoy', 'watch', 'listen', 'play']
            },
            'beauty': {
                'high': ['beauty', 'cosmetics', 'makeup', 'skincare', 'haircare',
                        'salon', 'spa', 'treatment', 'facial', 'manicure',
                        'pedicure', 'cosmetic', 'beautician', 'esthetician'],
                'medium': ['makeup', 'skincare', 'hair', 'nail', 'beauty', 'cosmetic',
                          'treatment', 'salon', 'spa', 'glamour', 'style'],
                'low': ['beauty', 'pretty', 'glam', 'style', 'look']
            },
            'home': {
                'high': ['home', 'furniture', 'decor', 'interior', 'design',
                        'appliance', 'kitchen', 'bathroom', 'bedroom', 'living',
                        'garden', 'lawn', 'patio', 'backyard', 'homeware'],
                'medium': ['furniture', 'decor', 'interior', 'appliance', 'kitchen',
                          'bathroom', 'garden', 'home', 'house', 'residential'],
                'low': ['home', 'house', 'decor', 'furniture', 'appliance']
            },
            'sports': {
                'high': ['sports', 'game', 'athletic', 'fitness', 'exercise',
                        'football', 'basketball', 'cricket', 'tennis', 'golf',
                        'swimming', 'running', 'cycling', 'workout', 'training'],
                'medium': ['game', 'play', 'athlete', 'team', 'coach', 'training',
                          'competition', 'match', 'tournament', 'championship'],
                'low': ['sport', 'game', 'play', 'win', 'lose']
            },
            'travel': {
                'high': ['travel', 'tourism', 'vacation', 'holiday', 'trip',
                        'journey', 'tour', 'destination', 'hotel', 'resort',
                        'flight', 'airline', 'booking', 'reservation', 'itinerary'],
                'medium': ['vacation', 'holiday', 'trip', 'tour', 'destination',
                          'hotel', 'flight', 'booking', 'travel', 'journey'],
                'low': ['travel', 'trip', 'tour', 'vacation', 'holiday']
            },
            'weapons': {
                'high': ['gun', 'rifle', 'pistol', 'firearm', 'ammunition',
                        'weapon', 'arm', 'combat', 'shooting', 'firearms', 'bullet',
                        'ammo', 'arsenal', 'military', 'war', 'battle'],
                'medium': ['bullet', 'ammo', 'arsenal', 'military', 'defense',
                          'attack', 'violent', 'dangerous', 'lethal', 'kill',
                          'shoot', 'aim', 'target', 'combat', 'warfare'],
                'low': ['bang', 'shoot', 'aim', 'target', 'kill', 'war', 'fight']
            },
            'drugs': {
                'high': ['drug', 'cocaine', 'heroin', 'marijuana', 'opioid',
                        'narcotic', 'addict', 'substance', 'overdose', 'illegal',
                        'weed', 'pill', 'medicine', 'pharmaceutical', 'narcotics'],
                'medium': ['weed', 'pill', 'medicine', 'prescription', 'pharmacy',
                          'addiction', 'rehab', 'treatment', 'abuse', 'high',
                          'stoned', 'doped', 'intoxicated', 'substance'],
                'low': ['high', 'stoned', 'doped', 'intoxicated', 'illegal', 'drug']
            },
            'adult_content': {
                'high': ['porn', 'xxx', 'explicit', 'adult', 'sexual',
                        'erotic', 'mature', 'nsfw', 'pornography', 'xxx',
                        'sex', 'intimate', 'adult only', 'explicit content'],
                'medium': ['sex', 'intimate', 'romance', 'dating', 'relationship',
                          'sensual', 'passion', 'desire', 'arousal', 'love',
                          'kiss', 'touch', 'feel', 'body', 'intimacy'],
                'low': ['love', 'kiss', 'touch', 'feel', 'body', 'romance', 'passion']
            },
            'gambling': {
                'high': ['casino', 'gambling', 'betting', 'poker', 'lottery',
                        'slot', 'wager', 'bet', 'odds', 'gamble', 'jackpot',
                        'winning', 'chance', 'betting', 'casino games'],
                'medium': ['jackpot', 'winning', 'chance', 'luck', 'fortune',
                          'game', 'play', 'risk', 'stake', 'payout', 'money',
                          'rich', 'win', 'lose', 'prize'],
                'low': ['money', 'rich', 'win', 'lose', 'prize', 'luck', 'chance']
            }
        }
        
        # Weight multipliers
        self.weights = {'high': 3, 'medium': 2, 'low': 1}
    
    def preprocess_text(self, text: str) -> List[str]:
        """Preprocess text for better keyword matching"""
        if not text:
            return []
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
            'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'having',
            'do', 'does', 'did', 'doing', 'this', 'that', 'these', 'those',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
            'will', 'would', 'should', 'could', 'might', 'must', 'can',
            'may', 'shall', 'ought', 'about', 'above', 'after', 'again',
            'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t',
            'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
            'between', 'both', 'but', 'by', 'can\'t', 'cannot', 'could',
            'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing',
            'don\'t', 'down', 'during', 'each', 'few', 'for', 'from', 'further',
            'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having',
            'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers',
            'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d',
            'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it',
            'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t',
            'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once',
            'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out',
            'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s',
            'should', 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s',
            'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
            'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re',
            'they\'ve', 'this', 'those', 'through', 'to', 'too', 'under',
            'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll',
            'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when',
            'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s',
            'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t',
            'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours',
            'yourself', 'yourselves'
        }
        
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return words
    
    def calculate_score(self, words: List[str], category: str) -> float:
        """Calculate score for a category based on keyword matches"""
        total_score = 0
        
        if category in self.keywords:
            for weight_level, keywords in self.keywords[category].items():
                weight = self.weights[weight_level]
                for keyword in keywords:
                    # Check for exact word match
                    if keyword in words:
                        total_score += weight
                        break  # Count each keyword only once
        
        return total_score
    
    def predict(self, text: str) -> Dict:
        """Complete keyword-based prediction with proper confidence"""
        # Preprocess text
        words = self.preprocess_text(text)
        
        if not words:
            return {
                'category': 'other',
                'confidence': 0.1,
                'is_restricted': False,
                'top_categories': [['other', 0.1]],
                'method': 'keyword_based'
            }
        
        # Calculate scores for each category
        scores = {}
        for category in self.keywords.keys():
            score = self.calculate_score(words, category)
            if score > 0:
                scores[category] = score
        
        # If no matches, return other
        if not scores:
            return {
                'category': 'other',
                'confidence': 0.1,
                'is_restricted': False,
                'top_categories': [['other', 0.1]],
                'method': 'keyword_based'
            }
        
        # Get best category
        best_category = max(scores.items(), key=lambda x: x[1])[0]
        best_score = scores[best_category]
        
        # Calculate normalized confidence (0.5 to 0.95)
        max_possible_score = sum(len(keywords) * self.weights[weight_level] 
                               for weight_level, keywords in self.keywords[best_category].items())
        
        if max_possible_score > 0:
            confidence = 0.5 + (0.45 * (best_score / max_possible_score))
            confidence = min(confidence, 0.95)  # Cap at 95%
            confidence = round(confidence, 2)   # Round to 2 decimal places
        else:
            confidence = 0.7
        
        # Get top 3 categories with their confidence
        top_categories = []
        for category, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]:
            max_for_cat = sum(len(keywords) * self.weights[weight_level] 
                            for weight_level, keywords in self.keywords[category].items())
            if max_for_cat > 0:
                cat_confidence = 0.5 + (0.45 * (score / max_for_cat))
                top_categories.append([category, min(round(cat_confidence, 2), 0.95)])
        
        return {
            'category': best_category,
            'confidence': confidence,
            'is_restricted': best_category in self.restricted_categories,
            'top_categories': top_categories,
            'method': 'keyword_based'
        }

# Test function
def test_classifier():
    """Test the classifier with various inputs"""
    classifier = TextClassifier()
    
    test_cases = [
        ("Latest fashion trends and electronic gadgets", ["fashion", "electronics"]),
        ("Software development using Python programming", ["tech"]),
        ("Restaurant food and cooking recipes", ["food"]),
        ("Medical treatment and healthcare services", ["health"]),
        ("Investment banking and stock trading", ["finance"]),
        ("Car engine and automotive parts", ["automotive"]),
        ("Real estate property and home buying", ["real_estate"]),
        ("Movie entertainment and music shows", ["entertainment"]),
        ("Beauty cosmetics and skincare products", ["beauty"]),
        ("Home furniture and interior design", ["home"]),
        ("Sports games and athletic training", ["sports"]),
        ("Travel tourism and vacation trips", ["travel"])
    ]
    
    print("🧪 Testing Complete Text Classifier")
    print("="*60)
    
    for text, expected_categories in test_cases:
        result = classifier.predict(text)
        print(f"\nText: {text}")
        print(f"✅ Predicted: {result['category']}")
        print(f"✅ Expected in: {expected_categories}")
        print(f"✅ Confidence: {result['confidence']:.2%}")
        print(f"✅ Is Restricted: {result['is_restricted']}")
        
        if result['top_categories']:
            print("✅ Top Categories:")
            for cat, conf in result['top_categories'][:3]:
                print(f"   - {cat}: {conf:.2%}")

if __name__ == "__main__":
    test_classifier()