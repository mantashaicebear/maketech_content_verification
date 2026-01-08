def fuse_results(text_res: dict, image_res: dict):
    """Combine text and image classifier outputs and return a final decision.

    Returns: {decision: 'allow'|'restrict', categories: [...], reasons: [...]}
    """
    categories = set()
    reasons = []

    for src, res in (("text", text_res), ("image", image_res)):
        if not res:
            continue
        for c in res.get("labels", []):
            categories.add(c)
        if res.get("labels"):
            reasons.append({"source": src, "labels": res.get("labels"), "score": res.get("score")})

    decision = "restrict" if categories else "allow"
    return {"decision": decision, "categories": sorted(categories), "reasons": reasons}
