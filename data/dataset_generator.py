"""
Dummy Dataset Generator for Content Verification
Creates realistic synthetic business content for classification.
"""

import pandas as pd
import random

# Sample texts for each category
SAMPLES = {
    "Food": [
        "Fresh organic vegetables, free home delivery available",
        "Best pizza in town with premium cheese and basil",
        "Coffee shop opening - finest quality beans imported",
        "Catering service for weddings and events",
        "Restaurant reservation system now online",
    ],
    "Tech": [
        "Latest smartphone with 5G and great camera",
        "Software update improves battery life",
        "Python programming course available",
        "Cloud storage solution secure and affordable",
        "New app reduces mobile data usage",
    ],
    "Education": [
        "Online degree program accredited and affordable",
        "Scholarship opportunities for students",
        "Data science certification course",
        "Language learning in 6 months",
        "Free webinar on career development",
    ],
    "Fashion": [
        "New winter collection sustainable fabrics",
        "50% discount on all accessories",
        "Custom tailoring service available",
        "Designer collaboration exclusive pieces",
        "Handcrafted jewelry with certified gemstones",
    ],
    "Finance": [
        "Invest in mutual funds with good returns",
        "Financial planning consultation for retirement",
        "Savings account with high interest rates",
        "Insurance plans for health and life",
        "Stock trading platform with zero fees",
    ],
    "Weapons": [
        "Military equipment for tactical training",
        "Firearms dealer licensed and authorized",
        "Body armor and helmets for professionals",
        "Ammunition supplier bulk orders accepted",
        "Combat training facility self defense courses",
    ],
    "Drugs": [
        "Pharmaceutical distributor licensed",
        "Online pharmacy medications available",
        "Herbal supplements natural remedies",
        "Pain relief medication available",
        "Drug testing kits available",
    ],
    "Explosives": [
        "Fireworks store licensed pyrotechnics",
        "Demolition services professional experts",
        "Quarry explosives for mining operations",
        "Dynamite manufacturer industrial use",
        "Explosive training courses available",
    ],
}

def create_dummy_dataset(samples_per_category=40, random_seed=42):
    """
    Create dataset with business content texts and categories.
    
    Args:
        samples_per_category: number of samples per category
        random_seed: for reproducibility
    
    Returns:
        DataFrame with 'text' and 'category' columns
    """
    random.seed(random_seed)
    data = []
    
    for category, texts in SAMPLES.items():
        for _ in range(samples_per_category):
            text = random.choice(texts)
            data.append({"text": text, "category": category})
    
    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)
    return df
if __name__ == "__main__":
    df = create_dummy_dataset(samples_per_category=40)
    print(f"Dataset created: {df.shape[0]} samples, {df['category'].nunique()} categories")
    print(df.head())
