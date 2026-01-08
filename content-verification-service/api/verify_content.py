from inference.text_classifier import classify_text
from inference.image_classifier import classify_image
from inference.fusion import fuse_predictions
from policy.decision_engine import decide
from database.business_profiles import get_business

def verify_content_api(
    business_id: str,
    text: str = None,
    image_path: str = None
) -> dict:
    """
    API function to verify posted content
    """
    business = get_business(business_id)
    if not business:
        return {"status": "ERROR", "message": "Business not found"}

    text_pred = classify_text(text) if text else None
    image_pred = classify_image(image_path) if image_path else None

    final_prediction = fuse_predictions(text_pred, image_pred)
    decision = decide(business, final_prediction)

    return {
        "business_id": business_id,
        "decision": decision
    }
