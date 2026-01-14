"""
Text Preprocessing - Clean and normalize business content.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except:
    nltk.download('wordnet')


def preprocess_text(text, lemmatize=True):
    """
    Clean text: lowercase, remove special chars, remove stopwords, lemmatize.
    
    Args:
        text: Raw text string
        lemmatize: Apply lemmatization (default True)
    
    Returns:
        Cleaned text string
    """
    # Lowercase
    text = text.lower()
    
    # Remove special characters, keep only letters and spaces
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Remove extra spaces
    text = ' '.join(text.split())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 1]
    
    # Lemmatize
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(w) for w in words]
    
    return ' '.join(words)


if __name__ == "__main__":
    text = "Hello! I'm selling PREMIUM coffee at $10/kg. Visit www.example.com!"
    cleaned = preprocess_text(text)
    print(f"Original: {text}")
    print(f"Cleaned: {cleaned}")
