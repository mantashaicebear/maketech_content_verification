"""
Final Dataset Generator - Creates dataset once with business_id, text, category, domain, etc.
Includes: single-domain businesses, multi-domain businesses, and restricted content samples
"""

import pandas as pd
import random

# Set seed for reproducibility
random.seed(42)

class FinalDatasetGenerator:
    def __init__(self):
        # Safe categories with keywords
        self.safe_categories = {
            'food': ['pizza', 'restaurant', 'recipe', 'cooking', 'meal', 'dish', 'eat', 'cuisine', 'grocery', 'dining'],
            'tech': ['software', 'coding', 'computer', 'technology', 'app', 'program', 'code', 'digital', 'AI', 'machine learning'],
            'education': ['learning', 'course', 'study', 'education', 'school', 'teach', 'university', 'training', 'tutorial', 'skills'],
            'health': ['medical', 'health', 'doctor', 'hospital', 'medicine', 'fitness', 'wellness', 'care', 'pharmacy', 'treatment'],
            'finance': ['investment', 'banking', 'loan', 'finance', 'money', 'stock', 'wealth', 'insurance', 'credit', 'savings'],
            'fashion': ['clothing', 'fashion', 'dress', 'style', 'wear', 'apparel', 'outfit', 'trend', 'accessories', 'jewelry'],
            'electronics': ['electronic', 'device', 'gadget', 'phone', 'laptop', 'camera', 'smart', 'mobile', 'tablet', 'TV'],
            'automotive': ['car', 'vehicle', 'auto', 'motor', 'drive', 'engine', 'transport', 'road', 'bike', 'motorcycle'],
            'real_estate': ['property', 'house', 'home', 'apartment', 'land', 'building', 'rent', 'buy', 'villa', 'flat'],
            'entertainment': ['movie', 'music', 'show', 'film', 'concert', 'performance', 'art', 'media', 'streaming', 'gaming'],
            'books': ['books', 'reading', 'literature', 'novel', 'publication', 'author', 'library', 'ebook', 'magazine', 'journal'],
            'travel': ['travel', 'tourism', 'hotel', 'vacation', 'flight', 'booking', 'tour', 'destination', 'resort', 'holiday'],
            'grocery': ['groceries', 'supermarket', 'vegetables', 'fruits', 'organic', 'fresh', 'daily needs', 'household', 'essentials'],
            'beauty': ['beauty', 'cosmetics', 'skincare', 'makeup', 'salon', 'spa', 'haircare', 'fragrance', 'grooming'],
            'sports': ['sports', 'fitness equipment', 'athletic', 'workout', 'gym', 'exercise', 'outdoor', 'team sports'],
        }
        
        # Restricted categories with keywords
        self.restricted_categories = {
            'weapons': ['gun', 'rifle', 'pistol', 'weapon', 'firearm', 'ammo', 'ammunition', 'bullet', 'explosive'],
            'drugs': ['drug', 'cocaine', 'heroin', 'marijuana', 'weed', 'narcotic', 'opioid', 'pill', 'illegal substance'],
            'adult_content': ['adult', 'porn', 'xxx', 'explicit', 'nsfw', 'sexual', 'erotic', 'mature'],
            'gambling': ['casino', 'betting', 'gamble', 'lottery', 'poker', 'slot', 'bet', 'wager', 'roulette'],
        }
        
        # Multi-domain businesses (marketplace style)
        self.multi_domain_businesses = {
            'M001': {'name': 'Amazon India', 'domains': ['electronics', 'fashion', 'books', 'grocery', 'beauty', 'sports', 'automotive', 'tech']},
            'M002': {'name': 'Flipkart', 'domains': ['electronics', 'fashion', 'books', 'grocery', 'beauty', 'sports', 'automotive']},
            'M003': {'name': 'Myntra', 'domains': ['fashion', 'beauty', 'sports']},
            'M004': {'name': 'Swiggy', 'domains': ['food', 'grocery']},
            'M005': {'name': 'Zomato', 'domains': ['food', 'grocery']},
            'M006': {'name': 'MakeMyTrip', 'domains': ['travel', 'entertainment']},
            'M007': {'name': 'BookMyShow', 'domains': ['entertainment', 'travel']},
            'M008': {'name': 'Nykaa', 'domains': ['beauty', 'fashion', 'health']},
        }
        
        # Single-domain businesses (specialized stores)
        self.single_domain_businesses = {}
        domains_list = list(self.safe_categories.keys())
        for i, domain in enumerate(domains_list):
            bid = f'B{i+1:03d}'
            self.single_domain_businesses[bid] = {'name': f'{domain.title()} Specialist {bid}', 'domains': [domain]}
        
        # Special case: B057 for education
        self.single_domain_businesses['B057'] = {'name': 'Education Specialist B057', 'domains': ['education']}
    
    def generate_text_sample(self, category):
        """Generate diverse text samples for a category"""
        keywords = self.safe_categories.get(category, [])
        if not keywords:
            keywords = self.restricted_categories.get(category, ['sample'])
        
        kw1 = random.choice(keywords)
        kw2 = random.choice(keywords)
        
        templates = [
            f"Amazing {kw1}! Perfect for {kw2} needs",
            f"Just launched our new {kw1} range",
            f"Looking for {kw1}? We've got you covered",
            f"Exclusive {kw1} deals - limited time offer",
            f"New arrival: Latest {kw1} collection",
            f"Shop now for premium {kw1} at great prices",
            f"Best {kw1} ever!",
            f"Order {kw1} online now",
            f"Premium {kw1} services available",
            f"Discover {kw1} and {kw2} today",
        ]
        return random.choice(templates)
    
    def generate_dataset(self, samples_per_category=150):
        """Generate comprehensive dataset"""
        data = []
        
        # Get all businesses
        all_businesses = {**self.multi_domain_businesses, **self.single_domain_businesses}
        
        print("Generating dataset with:")
        print(f"  - Multi-domain businesses: {len(self.multi_domain_businesses)}")
        print(f"  - Single-domain businesses: {len(self.single_domain_businesses)}")
        print(f"  - Samples per safe category: {samples_per_category}")
        print()
        
        # 1. SAFE CATEGORIES - Positive examples (allowed posts)
        print("Generating positive samples for safe categories...")
        for category in self.safe_categories.keys():
            # Get all businesses that allow this category
            eligible_businesses = [bid for bid, binfo in all_businesses.items() 
                                 if category in binfo['domains']]
            
            for _ in range(samples_per_category):
                business_id = random.choice(eligible_businesses)
                binfo = all_businesses[business_id]
                text = self.generate_text_sample(category)
                
                data.append({
                    'business_id': business_id,
                    'text': text,
                    'category': category,
                    'detected_domain': category,
                    'allowed_domains': ','.join(sorted(binfo['domains'])),
                    'is_allowed': 1
                })
        
        print(f"  ✓ Generated {len(self.safe_categories) * samples_per_category} positive samples")
        
        # 2. RESTRICTED CATEGORIES - Negative examples (blocked posts)
        print("Generating negative samples for restricted categories...")
        restricted_count = 0
        for restricted_cat in self.restricted_categories.keys():
            # Restricted content should be blocked for ALL businesses
            sample_businesses = random.sample(list(all_businesses.keys()), 
                                            min(30, len(all_businesses)))
            
            for business_id in sample_businesses:
                binfo = all_businesses[business_id]
                text = self.generate_text_sample(restricted_cat)
                
                data.append({
                    'business_id': business_id,
                    'text': text,
                    'category': restricted_cat,
                    'detected_domain': restricted_cat,
                    'allowed_domains': ','.join(sorted(binfo['domains'])),
                    'is_allowed': 0  # Always blocked
                })
                restricted_count += 1
        
        print(f"  ✓ Generated {restricted_count} restricted samples (all blocked)")
        
        # 3. DOMAIN MISMATCH - Business posts in non-allowed domain
        print("Generating domain mismatch samples...")
        mismatch_count = 0
        for business_id, binfo in list(all_businesses.items())[:40]:  # Sample of businesses
            allowed = binfo['domains']
            all_categories = list(self.safe_categories.keys())
            not_allowed = [cat for cat in all_categories if cat not in allowed]
            
            if not_allowed:
                # Pick a few mismatches for each business
                for _ in range(2):
                    category = random.choice(not_allowed)
                    text = self.generate_text_sample(category)
                    
                    data.append({
                        'business_id': business_id,
                        'text': text,
                        'category': category,
                        'detected_domain': category,
                        'allowed_domains': ','.join(sorted(allowed)),
                        'is_allowed': 0  # Domain mismatch - blocked
                    })
                    mismatch_count += 1
        
        print(f"  ✓ Generated {mismatch_count} domain mismatch samples")
        
        # 4. MULTI-DOMAIN SUCCESS - Businesses posting across their allowed domains
        print("Generating multi-domain samples...")
        multi_count = 0
        for business_id, binfo in self.multi_domain_businesses.items():
            for domain in binfo['domains']:
                for _ in range(5):  # Few samples per domain per business
                    text = self.generate_text_sample(domain)
                    
                    data.append({
                        'business_id': business_id,
                        'text': text,
                        'category': domain,
                        'detected_domain': domain,
                        'allowed_domains': ','.join(sorted(binfo['domains'])),
                        'is_allowed': 1
                    })
                    multi_count += 1
        
        print(f"  ✓ Generated {multi_count} multi-domain samples")
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Shuffle
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print(f"\nDataset Summary:")
        print(f"  Total samples: {len(df)}")
        print(f"  Allowed (1): {(df['is_allowed'] == 1).sum()}")
        print(f"  Blocked (0): {(df['is_allowed'] == 0).sum()}")
        print(f"  Unique businesses: {df['business_id'].nunique()}")
        print(f"  Unique categories: {df['category'].nunique()}")
        
        return df
    
    def save_dataset_and_profiles(self, df, dataset_path, profiles_path):
        """Save dataset and business profiles"""
        # Save dataset
        df.to_csv(dataset_path, index=False)
        print(f"\n✓ Dataset saved to: {dataset_path}")
        
        # Save business profiles as JSON
        all_businesses = {**self.multi_domain_businesses, **self.single_domain_businesses}
        import json
        
        with open(profiles_path, 'w') as f:
            json.dump(all_businesses, f, indent=2)
        
        print(f"✓ Business profiles saved to: {profiles_path}")
        
        # Print sample
        print(f"\nFirst 10 rows of dataset:")
        print(df.head(10).to_string())
        
        print(f"\nSample businesses:")
        for bid in ['M001', 'B001', 'B057']:
            if bid in all_businesses:
                binfo = all_businesses[bid]
                print(f"  {bid}: {binfo['name']} → {binfo['domains']}")


if __name__ == "__main__":
    generator = FinalDatasetGenerator()
    df = generator.generate_dataset(samples_per_category=150)
    
    dataset_path = "content_verification_dataset.csv"
    profiles_path = "business_profiles.json"
    
    generator.save_dataset_and_profiles(df, dataset_path, profiles_path)
    
    print("\n" + "="*50)
    print("✓ Dataset generation COMPLETE")
    print("="*50)
