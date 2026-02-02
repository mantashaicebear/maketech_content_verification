"""
Dataset Generator for Content Verification
"""

import pandas as pd
import random
import json
from typing import List, Dict

class DatasetGenerator:
    """Generate synthetic dataset for training with business IDs and domains"""
    
    # Restricted categories that no business should post
    RESTRICTED_CATEGORIES = ['weapons', 'drugs', 'adult_content', 'gambling']
    
    # Safe categories that businesses can operate in
    SAFE_CATEGORIES = {
        'food': ['food', 'restaurant', 'recipe', 'cooking', 'meal', 'dish', 'eat', 'cuisine', 'grocery', 'dining', 'catering', 'bakery', 'cafe'],
        'tech': ['software', 'coding', 'computer', 'technology', 'app', 'program', 'code', 'digital', 'cloud', 'AI', 'machine learning', 'data', 'analytics'],
        'education': ['learning', 'course', 'study', 'education', 'school', 'teach', 'learn', 'university', 'training', 'tutorial', 'certification', 'skills'],
        'health': ['medical', 'health', 'doctor', 'hospital', 'medicine', 'fitness', 'wellness', 'care', 'pharmacy', 'diagnosis', 'treatment', 'yoga'],
        'finance': ['investment', 'banking', 'loan', 'finance', 'money', 'stock', 'cash', 'wealth', 'insurance', 'credit', 'savings', 'payment'],
        'fashion': ['clothing', 'fashion', 'dress', 'style', 'wear', 'apparel', 'outfit', 'trend', 'accessories', 'jewelry', 'footwear', 'designer'],
        'electronics': ['electronic', 'device', 'gadget', 'phone', 'laptop', 'camera', 'smart', 'tech', 'appliance', 'mobile', 'tablet', 'TV', 'smartphone', 'smart home', 'smart devices', 'home automation', 'electronic devices', 'Alexa', 'Google Home'],
        'automotive': ['car', 'vehicle', 'auto', 'motor', 'drive', 'engine', 'transport', 'road', 'bike', 'motorcycle', 'parts', 'service'],
        'real_estate': ['property', 'house', 'home', 'apartment', 'land', 'building', 'rent', 'buy', 'villa', 'flat', 'commercial', 'residential'],
        'entertainment': ['movie', 'music', 'show', 'film', 'concert', 'performance', 'art', 'media', 'streaming', 'gaming', 'events', 'sports'],
        'books': ['books', 'reading', 'literature', 'novel', 'publication', 'author', 'library', 'ebook', 'magazine', 'journal'],
        'travel': ['travel', 'tourism', 'hotel', 'vacation', 'flight', 'booking', 'tour', 'destination', 'resort', 'holiday'],
        'grocery': ['groceries', 'supermarket', 'vegetables', 'fruits', 'organic', 'fresh', 'daily needs', 'household', 'essentials'],
        'beauty': ['beauty', 'cosmetics', 'skincare', 'makeup', 'salon', 'spa', 'haircare', 'fragrance', 'grooming'],
        'sports': ['sports', 'fitness equipment', 'athletic', 'workout', 'gym', 'exercise', 'outdoor', 'team sports'],
    }
    
    # All categories including restricted ones
    ALL_CATEGORIES = {
        **SAFE_CATEGORIES,
        'weapons': ['gun', 'rifle', 'pistol', 'weapon', 'firearm', 'ammo', 'ammunition', 'bullet', 'combat', 'explosive', 'knife', 'firearms', 'rifles', 'pistols', 'guns', 'ak47', 'shotgun', 'revolver', 'assault rifle', 'handgun', 'military weapon'],
        'drugs': ['drug', 'cocaine', 'heroin', 'marijuana', 'weed', 'narcotic', 'opioid', 'pill', 'substance', 'illegal'],
        'adult_content': ['adult', 'porn', 'xxx', 'explicit', 'nsfw', 'sexual', 'erotic', 'mature', 'nude', 'intimate'],
        'gambling': ['casino', 'betting', 'gamble', 'lottery', 'poker', 'slot', 'bet', 'wager', 'roulette', 'jackpot']
    }
    
    # Real Indian multi-domain businesses (marketplaces)
    INDIAN_MARKETPLACES = {
        'AMAZON_IN': {
            'name': 'Amazon India',
            'domains': ['electronics', 'fashion', 'books', 'grocery', 'beauty', 'sports', 'automotive', 'tech'],
            'type': 'mega-marketplace'
        },
        'FLIPKART': {
            'name': 'Flipkart',
            'domains': ['electronics', 'fashion', 'books', 'grocery', 'beauty', 'sports', 'automotive'],
            'type': 'mega-marketplace'
        },
        'RELIANCE': {
            'name': 'Reliance Digital & JioMart',
            'domains': ['electronics', 'grocery', 'fashion', 'beauty', 'tech'],
            'type': 'mega-marketplace'
        },
        'TATA_NEU': {
            'name': 'Tata Neu',
            'domains': ['electronics', 'fashion', 'grocery', 'travel', 'food', 'beauty'],
            'type': 'mega-marketplace'
        },
        'MYNTRA': {
            'name': 'Myntra',
            'domains': ['fashion', 'beauty', 'sports'],
            'type': 'marketplace'
        },
        'SWIGGY': {
            'name': 'Swiggy',
            'domains': ['food', 'grocery'],
            'type': 'marketplace'
        },
        'ZOMATO': {
            'name': 'Zomato',
            'domains': ['food', 'grocery'],
            'type': 'marketplace'
        },
        'PAYTM': {
            'name': 'Paytm Mall',
            'domains': ['electronics', 'fashion', 'grocery', 'travel', 'finance'],
            'type': 'marketplace'
        },
        'MEESHO': {
            'name': 'Meesho',
            'domains': ['fashion', 'beauty', 'electronics', 'grocery'],
            'type': 'marketplace'
        },
        'NYKAA': {
            'name': 'Nykaa',
            'domains': ['beauty', 'fashion', 'health'],
            'type': 'marketplace'
        },
        'BIGBASKET': {
            'name': 'BigBasket',
            'domains': ['grocery', 'food', 'beauty', 'health'],
            'type': 'marketplace'
        },
        'SNAPDEAL': {
            'name': 'Snapdeal',
            'domains': ['electronics', 'fashion', 'books', 'sports'],
            'type': 'marketplace'
        },
        'MAKEMYTRIP': {
            'name': 'MakeMyTrip',
            'domains': ['travel', 'entertainment'],
            'type': 'marketplace'
        },
        'BOOKMYSHOW': {
            'name': 'BookMyShow',
            'domains': ['entertainment', 'travel'],
            'type': 'marketplace'
        }
    }
    
    def __init__(self):
        self.categories = self.ALL_CATEGORIES
        self.businesses = {}
        self.business_counter = 0
    
    def generate_business_id(self, domain: str) -> str:
        """Generate a business ID"""
        self.business_counter += 1
        return f"B{self.business_counter:03d}"
    
    def create_businesses(self, num_single_domain: int = 30, num_small_multi_domain: int = 15) -> Dict:
        """Create businesses with assigned IDs (numeric IDs for all, names for multi-domain)"""
        businesses = {}
        business_counter = 1
        
        # Add real Indian marketplaces first (multi-domain with assigned IDs)
        for marketplace_id, marketplace_info in self.INDIAN_MARKETPLACES.items():
            assigned_id = f"M{business_counter:03d}"  # M001, M002, etc. for multi-domain
            businesses[assigned_id] = {
                'id': assigned_id,
                'original_id': marketplace_id,  # Keep original for reference
                'domains': marketplace_info['domains'],
                'type': marketplace_info['type'],
                'name': marketplace_info['name']  # Keep name for multi-domain businesses
            }
            business_counter += 1
        
        # Single-domain businesses (local businesses, specialized stores)
        # Ensure B057 is assigned to education domain
        for i in range(num_single_domain):
            business_id = self.generate_business_id("single")
            
            # B057 = B001 + 56, so index 56 out of 0-based
            # Since we now generate num_single_domain businesses, B057 exists only if num >= 57
            # business_id auto-generates B001, B002, ..., so counter-1 = index
            # When business_counter = 57, business_id = "B057"
            # At that point, i would be... let's see:
            # i starts at 0 when counter=15 (after 14 marketplaces)
            # When i = 42, business_counter becomes 57, business_id = "B057"
            if business_id == "B057":
                domain = 'education'
            else:
                domain = random.choice(list(self.SAFE_CATEGORIES.keys()))
            
            businesses[business_id] = {
                'id': business_id,
                'domains': [domain],
                'type': 'single-domain',
                'name': f"{domain.replace('_', ' ').title()} Specialist {business_id}"
            }
        
        # Small multi-domain businesses (2-3 domains, like local stores with multiple categories)
        for _ in range(num_small_multi_domain):
            assigned_id = f"M{business_counter:03d}"  # M010, M011, etc.
            num_domains = random.randint(2, 3)
            domains = random.sample(list(self.SAFE_CATEGORIES.keys()), num_domains)
            name = f"Multi-Category Store M{business_counter:03d}"  # Keep name for multi-domain
            businesses[assigned_id] = {
                'id': assigned_id,
                'domains': domains,
                'type': 'small-marketplace',
                'name': name  # Keep name for multi-domain
            }
            business_counter += 1
        
        self.businesses = businesses
        return businesses
    
    def generate_text(self, category: str) -> str:
        """Generate realistic, varied text matching real-world posts"""
        keywords = self.categories.get(category, [])
        if not keywords:
            return f"This is a sample text about {category}"
        
        kw1 = random.choice(keywords)
        kw2 = random.choice(keywords)
        kw3 = random.choice(keywords)
        
        # 60+ highly varied templates matching real-world posts, social media, and e-commerce
        templates = [
            # Natural conversational style
            f"Amazing {kw1}! Perfect for {kw2} needs",
            f"Just launched our new {kw1} range",
            f"Loving our {kw1} collection! Great for {kw2}",
            f"Looking for {kw1}? We've got you covered",
            f"Our new {kw1} with {kw2} features",
            f"Fresh {kw1} delivered daily",
            f"Exclusive {kw1} with advanced {kw2}",
            
            # Product descriptions (e-commerce style)
            f"New AI-powered {kw1} with {kw2} integration",
            f"Latest {kw1} collection with {kw2} technology",
            f"Premium {kw1} products for {kw2} enthusiasts",
            f"Designer {kw1} with trendy {kw2}",
            f"Organic {kw1} and fresh {kw2}",
            f"Smart {kw1} devices with {kw2} capabilities",
            f"Professional {kw1} equipment for {kw2}",
            
            # Short social media posts
            f"Best {kw1} ever!",
            f"New {kw1} alert!",
            f"{kw1} for {kw2}",
            f"Check out this {kw1}",
            f"Amazing {kw1} deals",
            f"Top {kw1} picks",
            
            # Service offerings
            f"We provide services for {kw1} in {category} industry",
            f"Premium {kw1} services available now",
            f"Get the best {kw1} and {kw2} services today",
            f"Quality {kw1} products at affordable prices",
            f"Professional {kw1} and {kw2} solutions",
            
            # Marketing/promotional
            f"Exclusive {kw1} deals - limited time offer",
            f"New arrival: Latest {kw1} and {kw2} collection",
            f"Hot sale on {kw1} - up to 50% off",
            f"Shop now for premium {kw1} at great prices",
            f"Special offer on {kw1} and {kw2}",
            f"Book your {kw1} with {kw2} packages",
            
            # Educational/informational
            f"Learn more about {kw1} for {category} enthusiasts",
            f"Everything you need to know about {kw1} and {kw2}",
            f"Expert guide to {kw1} and {kw2}",
            f"Understanding {kw1} for better {kw2}",
            
            # Benefits-focused
            f"Best {kw1} solutions for your {category} needs",
            f"Transform your experience with {kw1}",
            f"Revolutionary {kw1} technology for {kw2}",
            f"Innovative {kw1} designed for {kw2} lovers",
            
            # Real-world marketplace style
            f"Bestselling {kw1} for {kw2} enthusiasts",
            f"Delicious {kw1} and {kw2} delivered hot",
            f"Explore {kw1} options for {kw2}",
            f"Discover {kw1} and {kw2} today",
            
            # Customer testimonial style
            f"Your trusted source for {kw1} and {kw2}",
            f"Join thousands who love our {kw1} products",
            f"Experience the difference with our {kw1}",
            f"Customer-approved {kw1} for {kw2}",
            
            # Action-oriented
            f"Order {kw1} online now",
            f"Browse our {kw1} collection",
            f"Shop {kw1} and {kw2}",
            f"Find the perfect {kw1}",
            f"Get instant access to {kw1}",
            
            # Feature highlights
            f"Advanced {kw1} with {kw2} features",
            f"High-quality {kw1} and {kw2}",
            f"State-of-the-art {kw1} technology",
            f"Cutting-edge {kw1} solutions",
        ]
        
        return random.choice(templates)
    
    def generate_dataset_with_business_ids(self, samples_per_category: int = 300) -> pd.DataFrame:
        """Generate dataset with business IDs and domain validation (domain-specific assignment)"""
        # Create businesses first (45 single-domain to include B057, 14 multi-domain)
        self.create_businesses(num_single_domain=45, num_small_multi_domain=0)
        
        # Create domain-to-business mapping (assign specific businesses to specific domains)
        domain_to_businesses = {}
        for business_id, binfo in self.businesses.items():
            for domain in binfo['domains']:
                if domain not in domain_to_businesses:
                    domain_to_businesses[domain] = []
                domain_to_businesses[domain].append(business_id)
        
        data = []
        
        # Generate data for SAFE categories only - using domain-specific business assignment
        for category in self.SAFE_CATEGORIES.keys():
            # Get businesses assigned to this specific category
            eligible_businesses = domain_to_businesses.get(category, [])
            
            if not eligible_businesses:
                # Fallback: create a new business for this category
                business_id = self.generate_business_id("domain_specific")
                self.businesses[business_id] = {
                    'id': business_id,
                    'domains': [category],
                    'type': 'single-domain',
                    'name': f"{category.title()} Specialist"
                }
                eligible_businesses = [business_id]
                domain_to_businesses[category] = [business_id]
            
            # Use first business consistently for each category (not random)
            # This ensures predictable domain-business mappings
            primary_business = eligible_businesses[0]
            binfo = self.businesses[primary_business]
            allowed_domains_set = sorted(binfo['domains'])
            
            # STRICT VALIDATION: Ensure category is actually in allowed_domains
            if category not in binfo['domains']:
                raise ValueError(f"ERROR: Business {primary_business} being assigned to category {category}, "
                                f"but {category} is NOT in allowed_domains: {allowed_domains_set}")
            
            for _ in range(samples_per_category):
                text = self.generate_text(category)
                
                # All businesses show their allowed domains (comma-separated for multi-domain)
                allowed_str = ','.join(allowed_domains_set)
                
                data.append({
                    'text': text,
                    'category': category,
                    'business_id': primary_business,
                    'domain': category,
                    'allowed_domains': allowed_str,
                    'label': category,
                    'is_allowed': 1  # This business is allowed to post this content
                })
        
        # Generate test cases: RESTRICTED content (should always be blocked)
        for restricted_category in self.RESTRICTED_CATEGORIES:
            # Sample businesses across all types for restricted content
            sample_businesses = random.sample(list(self.businesses.keys()), 
                                           min(59, len(self.businesses)))
            for business_id in sample_businesses:
                text = self.generate_text(restricted_category)
                binfo = self.businesses[business_id]
                allowed_str = ','.join(sorted(binfo['domains']))
                
                data.append({
                    'text': text,
                    'category': restricted_category,
                    'business_id': business_id,
                    'domain': restricted_category,
                    'allowed_domains': allowed_str,
                    'label': restricted_category,
                    'is_allowed': 0  # Restricted content - should be blocked
                })
        
        # Generate test cases: Cross-domain violations (business posts outside allowed domain)
        for business_id, binfo in self.businesses.items():
            allowed_domains = sorted(binfo['domains'])
            not_allowed_domains = sorted(set(self.SAFE_CATEGORIES.keys()) - set(binfo['domains']))
            
            # Generate violations where business posts in NOT allowed domains
            num_violations = 5 if binfo['type'] == 'single-domain' else 3
            for _ in range(num_violations):
                if not_allowed_domains:
                    category = random.choice(not_allowed_domains)
                    text = self.generate_text(category)
                    allowed_str = ','.join(allowed_domains)
                    
                    data.append({
                        'text': text,
                        'category': category,
                        'business_id': business_id,
                        'domain': category,
                        'allowed_domains': allowed_str,
                        'label': category,
                        'is_allowed': 0  # Cross-domain violation
                    })
        
        # Generate positive examples for multi-domain businesses across their allowed domains
        for business_id, binfo in self.businesses.items():
            if binfo['type'] in ['marketplace', 'small-marketplace', 'mega-marketplace']:
                # Generate more samples for multi-domain businesses
                samples_per_domain = 30 if binfo['type'] == 'mega-marketplace' else 20
                allowed_domains = sorted(binfo['domains'])
                allowed_str = ','.join(allowed_domains)
                
                for domain in allowed_domains:
                    for _ in range(samples_per_domain):
                        text = self.generate_text(domain)
                        data.append({
                            'text': text,
                            'category': domain,
                            'business_id': business_id,
                            'domain': domain,
                            'allowed_domains': allowed_str,
                            'label': domain,
                            'is_allowed': 1  # Multi-domain business posting in allowed domain
                        })
        
        df = pd.DataFrame(data)
        # Shuffle the dataset
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return df
    
    def save_dataset(self, df: pd.DataFrame, filepath: str):
        """Save dataset to CSV file"""
        df.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
        print(f"Total samples: {len(df)}")
        print(f"Categories: {df['category'].nunique()}")
        print(f"Business IDs: {df['business_id'].nunique()}")
        print(f"\nCategory distribution:")
        print(df['category'].value_counts().sort_index())
        print(f"\nAllowed vs Blocked:")
        print(df['is_allowed'].value_counts())
    
    def save_business_profiles(self, filepath: str):
        """Save business profiles to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.businesses, f, indent=2)
        print(f"\nBusiness profiles saved to {filepath}")
        print(f"Total businesses created: {len(self.businesses)}")
        for bid, binfo in list(self.businesses.items())[:10]:
            print(f"  {bid}: {binfo['name']} - {binfo['domains']}")


if __name__ == "__main__":
    # Initialize the generator
    generator = DatasetGenerator()
    
    # Generate businesses with single and multi-domain support
    print("Creating business profiles...")
    print("Including real Indian marketplaces: Amazon, Flipkart, Reliance, Tata Neu, Myntra, etc.")
    businesses = generator.create_businesses(num_single_domain=30, num_small_multi_domain=15)
    print(f"Created {len(businesses)} businesses\n")
    
    # Count business types
    marketplace_count = sum(1 for b in businesses.values() if 'marketplace' in b['type'].lower())
    single_domain_count = sum(1 for b in businesses.values() if b['type'] == 'single-domain')
    print(f"  - Mega/Multi-domain marketplaces: {marketplace_count}")
    print(f"  - Single-domain businesses: {single_domain_count}\n")
    
    # Generate dataset with business IDs and domain validation
    print("Generating enhanced dataset with business IDs...")
    print("Using 300 samples per category for maximum accuracy...")
    dataset = generator.generate_dataset_with_business_ids(samples_per_category=300)
    
    # Save dataset to CSV
    dataset_path = "content_verification_dataset.csv"
    generator.save_dataset(dataset, dataset_path)
    
    # Save business profiles to JSON
    business_profiles_path = "business_profiles.json"
    generator.save_business_profiles(business_profiles_path)
    
    print("\nDataset generation complete!")
    print(f"\nFirst few samples:")
    print(dataset.head(15))
    
    print(f"\n\nReal Indian Marketplace Examples:")
    for bid, binfo in businesses.items():
        if 'marketplace' in binfo['type'].lower() and bid in generator.INDIAN_MARKETPLACES:
            print(f"\n{bid}:")
            print(f"  Name: {binfo['name']}")
            print(f"  Type: {binfo['type']}")
            print(f"  Allowed Domains ({len(binfo['domains'])}): {', '.join(binfo['domains'])}")
            break