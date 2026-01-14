import json

with open("policy/restricted_categories.json") as f:
    POLICY = json.load(f)

RESTRICTED = set(POLICY["restricted_categories"])

CONFIDENCE_THRESHOLD = 0.6

def decide(business: dict, prediction: dict) -> dict:
    """
    Core decision logic for content verification
    """

    if prediction["confidence"] < CONFIDENCE_THRESHOLD:
        return {
            "status": "WARN",
            "reason": "Low confidence classification",
            "prediction": prediction
        }

    # Single-domain business
    if business["business_type"] == "SingleDomain":
        if prediction["domain"] == business["allowed_domains"][0]:
            return {"status": "ALLOW", "prediction": prediction}
        else:
            return {
                "status": "BLOCK",
                "reason": "Domain mismatch",
                "prediction": prediction
            }

    # Marketplace business
    if business["business_type"] == "Marketplace":
        if prediction["domain"] in RESTRICTED:
            return {
                "status": "BLOCK",
                "reason": "Restricted marketplace category",
                "prediction": prediction
            }
        return {"status": "ALLOW", "prediction": prediction}

    return {"status": "BLOCK", "reason": "Invalid business type"}
