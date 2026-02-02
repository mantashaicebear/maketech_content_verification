# Project Overview

## Purpose
This project provides an AI-powered content verification service for business platforms. It validates posts against domain rules, blocks restricted content, and supports text and image moderation.

## High-Level Flow
1. **API request**
   - Full service API: [main.py](main.py) exposes /verify/text, /verify/image, /verify/mixed, and business/profile endpoints.
   - Text-only moderation API: [content-verify-&-decision-predict/app/main.py](content-verify-&-decision-predict/app/main.py) exposes /analyze.
2. **Text processing and inference**
   - Text is preprocessed, vectorized, and classified for category. Decision model predicts allowed/blocked probability. See [content-verify-&-decision-predict/app/trained_model_analyzer.py](content-verify-&-decision-predict/app/trained_model_analyzer.py).
3. **Business rules and domain enforcement**
   - For text-only API, detected category must match registered domain and be allowed for the business.
   - For full service API, business policies are applied through [policy/decision_engine.py](policy/decision_engine.py) and business profiles from [database/business_profiles.py](database/business_profiles.py).
4. **Response**
   - Returns status, reason, confidence, detected category, and domain checks.

## Tech Stack
- **Backend**: FastAPI, Uvicorn
- **ML/NLP**: scikit-learn (RandomForest, LogisticRegression), TF‑IDF vectorizer
- **Data**: pandas, numpy
- **Image**: torch, torchvision, PIL
- **Validation**: Pydantic models in [content-verify-&-decision-predict/app/models.py](content-verify-&-decision-predict/app/models.py)

## Core Components
- **Text moderation API**: [content-verify-&-decision-predict/app/main.py](content-verify-&-decision-predict/app/main.py)
- **Text analyzer (trained models)**: [content-verify-&-decision-predict/app/trained_model_analyzer.py](content-verify-&-decision-predict/app/trained_model_analyzer.py)
- **Full verification API (text, image, mixed)**: [main.py](main.py)
- **Verification orchestration**: [api/verify_content.py](api/verify_content.py)
- **Business rules**: [policy/decision_engine.py](policy/decision_engine.py)
- **Business profiles**: [database/business_profiles.py](database/business_profiles.py) and [data/business_profiles.json](data/business_profiles.json)
- **Training pipeline**: [train_models.py](train_models.py)
- **Trained artifacts**: [models/trained](models/trained)

## Operational Notes
- The text-only API enforces strict domain matching: detected category must equal the registered domain and be allowed for the business.
- Restricted categories (weapons, drugs, adult_content, gambling) are always blocked.
- For training, the current dataset is loaded from [data/content_verification_dataset.csv](data/content_verification_dataset.csv).
