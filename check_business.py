import json
import pandas as pd

# Load business profiles
with open('data/business_profiles.json') as f:
    data = json.load(f)

print('B053 profile:', data.get('B053', 'NOT FOUND'))
print()

# Find education businesses
edu_biz = [bid for bid, binfo in data.items() if 'education' in binfo.get('domains', [])]
print(f'Education businesses ({len(edu_biz)}):')
for bid in sorted(edu_biz)[:10]:
    print(f'  {bid}: {data[bid]["domains"]}')

print()

# Check dataset
df = pd.read_csv('data/content_verification_dataset.csv')
print(f'Total samples: {len(df)}')

# Show M001 samples by category
print('\nM001 samples by category:')
m001_cats = df[df['business_id'] == 'M001'].groupby('category').size().sort_values(ascending=False)
print(m001_cats)

# Verify M001 never has education
m001_edu = df[(df['business_id'] == 'M001') & (df['category'] == 'education')]
print(f'\nM001 with education category: {len(m001_edu)} (should be 0)')

# Check first education business
edu_bid = edu_biz[0] if edu_biz else None
if edu_bid:
    print(f'\n{edu_bid} samples by category:')
    edu_df = df[df['business_id'] == edu_bid]
    print(edu_df['category'].value_counts())
