class ImageModel:
    """Placeholder image model that inspects the image path for keywords."""

    def __init__(self):
        self.name = "placeholder-image-model"

    def predict(self, image_path: str):
        # Very naive heuristic based on filename
        labels = []
        if not image_path:
            return {"labels": labels, "score": 0.0}
        lower = image_path.lower()
        if any(w in lower for w in ("adult", "porn", "nsfw")):
            labels.append("sexual")
        if any(w in lower for w in ("violence", "blood", "gore")):
            labels.append("violence")
        if any(w in lower for w in ("hate", "racist", "slur")):
            labels.append("hate")
        score = 0.85 if labels else 0.05
        return {"labels": labels, "score": score}
