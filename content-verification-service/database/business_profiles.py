# Simulated DB access (replace with MongoDB later)

BUSINESSES = {
    "B001": {
        "business_id": "B001",
        "business_type": "SingleDomain",
        "allowed_domains": ["Automobile"]
    },
    "B002": {
        "business_id": "B002",
        "business_type": "Marketplace",
        "allowed_domains": ["Electronics", "Fashion"],
        "restricted_domains": []
    }
}

def get_business(business_id: str) -> dict:
    return BUSINESSES.get(business_id)
