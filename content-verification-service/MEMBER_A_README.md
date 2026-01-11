# Member A: Dataset, Preprocessing, Vectorization

This module creates dummy data, preprocesses text, and vectorizes it for classification.

## Files

- **dataset_generator.py** - Creates realistic synthetic business content (360 samples, 9 categories)
- **text_preprocessor.py** - Cleans text (lowercase, remove punctuation, stopwords, lemmatize)
- **text_vectorizer.py** - Converts text to TF-IDF features

## Usage

```python
from data import create_dummy_dataset
from data.text_preprocessor import preprocess_text
from data.text_vectorizer import vectorize_text

# 1. Create dataset
df = create_dummy_dataset(samples_per_category=40)

# 2. Preprocess text
df['cleaned'] = df['text'].apply(preprocess_text)

# 3. Vectorize
X, features, vectorizer = vectorize_text(df['cleaned'])

print(f"Feature matrix shape: {X.shape}")
print(f"Number of features: {len(features)}")
```

## Categories

**Normal (5):** Food, Tech, Education, Fashion, Finance  
**Restricted (4):** Weapons, Drugs, Explosives, Surveillance

## Output

- `X`: Feature matrix (sparse, TF-IDF values)
- `features`: Feature names (vocabulary)
- `vectorizer`: Fitted vectorizer for new data

Use this output with Member B for classification model training.
