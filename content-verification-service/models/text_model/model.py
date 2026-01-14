class TextModel:
    """Very small placeholder text model using keyword matching."""

    def __init__(self):
        self.name = "placeholder-text-model"

    def predict(self, text: str):
        # returns a simple score and raw labels derived from words
        text_lower = (text or "").lower()
        labels = []
        if any(w in text_lower for w in ("sex", "porn", "adult")):
            labels.append("sexual")
        if any(w in text_lower for w in ("hate", "racist", "slur")):
            labels.append("hate")
        if any(w in text_lower for w in ("kill", "murder", "blood")):
            labels.append("violence")
        score = 0.9 if labels else 0.1
        return {"labels": labels, "score": score}
