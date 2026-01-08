# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

# MODEL_PATH = "models/text_model"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
# model.eval()

# def classify_text(text: str) -> dict:
#     """
#     Classifies text into a business domain
#     """
#     inputs = tokenizer(
#         text,
#         return_tensors="pt",
#         truncation=True,
#         padding=True
#     )

#     with torch.no_grad():
#         outputs = model(**inputs)

#     probs = torch.softmax(outputs.logits, dim=1)
#     confidence, label_id = torch.max(probs, dim=1)

#     return {
#         "type": "text",
#         "domain": model.config.id2label[label_id.item()],
#         "confidence": round(confidence.item(), 3)
#     }
def classify_text(text: str) -> dict:
    text = text.lower()

    if "engine" in text or "car" in text or "automobile" in text:
        return {
            "type": "text",
            "domain": "Automobile",
            "confidence": 0.92
        }

    if "crypto" in text or "bitcoin" in text:
        return {
            "type": "text",
            "domain": "Crypto",
            "confidence": 0.95
        }

    if "gun" in text or "weapon" in text:
        return {
            "type": "text",
            "domain": "Weapons",
            "confidence": 0.97
        }

    return {
        "type": "text",
        "domain": "Unknown",
        "confidence": 0.45
    }
