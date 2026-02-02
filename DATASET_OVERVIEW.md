# Dataset Overview

## Location
- Dataset file: [data/content_verification_dataset.csv](data/content_verification_dataset.csv)
- Generator: [data/final_dataset_generator.py](data/final_dataset_generator.py)
- Business profiles: [data/business_profiles.json](data/business_profiles.json)

## Columns
- **business_id**: Business identifier (single-domain B###, multi-domain M###)
- **text**: Post content
- **category**: Ground-truth category for the post
- **detected_domain**: Same as category for training labels
- **allowed_domains**: Comma-separated list of domains allowed for the business
- **is_allowed**: 1 = allowed, 0 = blocked

## Category Coverage
- **Safe categories** (15): food, tech, education, health, finance, fashion, electronics, automotive, real_estate, entertainment, books, travel, grocery, beauty, sports
- **Restricted categories** (4): weapons, drugs, adult_content, gambling

## Business Coverage
- **Multi-domain businesses**: M001–M008 (marketplaces)
- **Single-domain businesses**: B001–B016 plus B057 (education specialist)

## Sample Types Included
- **Allowed posts**: Safe-category content where the business allows the domain
- **Restricted posts**: Restricted-category content (always blocked)
- **Domain mismatches**: Safe-category content posted by a business not allowed in that domain
- **Multi-domain positives**: Posts across each allowed domain for multi-domain businesses

## Generation Notes
- The dataset is generated once and saved to CSV by [data/final_dataset_generator.py](data/final_dataset_generator.py).
- The generator also writes business profiles to [data/business_profiles.json](data/business_profiles.json).
- The training pipeline loads this dataset directly in [train_models.py](train_models.py).
