"""
Business Profiles Database for Content Verification
"""

import json
import os
from typing import Dict, Optional

class BusinessProfileDB:
    """Business profiles database"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or "database/business_profiles.json"
        self.profiles = self._load_profiles()
    
    def _load_profiles(self) -> Dict:
        """Load profiles from file or use defaults"""
        default_profiles = {
            "B001": {
                "id": "B001",
                "business_name": "Tech Solutions Inc",
                "business_type": "single_domain",
                "business_domain": "tech",
                "allowed_domains": ["tech"],
                "is_verified": True,
                "verification_date": "2024-01-15",
                "registration_number": "TECH001",
                "owner_id": "U001"
            },
            "B002": {
                "id": "B002",
                "business_name": "Food Paradise",
                "business_type": "single_domain",
                "business_domain": "food",
                "allowed_domains": ["food"],
                "is_verified": True,
                "verification_date": "2024-01-20",
                "registration_number": "FOOD001",
                "owner_id": "U002"
            },
            "B003": {
                "id": "B003",
                "business_name": "Marketplace Hub",
                "business_type": "marketplace",
                "business_domain": "multi",
                "allowed_domains": ["tech", "fashion", "electronics", "home", "education"],
                "is_verified": True,
                "verification_date": "2024-01-25",
                "registration_number": "MKT001",
                "owner_id": "U003"
            },
            "B004": {
                "id": "B004",
                "business_name": "Health First Clinic",
                "business_type": "single_domain",
                "business_domain": "health",
                "allowed_domains": ["health"],
                "is_verified": True,
                "verification_date": "2024-02-01",
                "registration_number": "HLTH001",
                "owner_id": "U004"
            },
            "B005": {
                "id": "B005",
                "business_name": "Finance Experts",
                "business_type": "single_domain",
                "business_domain": "finance",
                "allowed_domains": ["finance"],
                "is_verified": True,
                "verification_date": "2024-02-05",
                "registration_number": "FIN001",
                "owner_id": "U005"
            }
        }
        
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    profiles = json.load(f)
                default_profiles.update(profiles)
        except:
            pass
        
        return default_profiles
    
    def get_profile(self, business_id: str) -> Optional[Dict]:
        """Get business profile by ID"""
        return self.profiles.get(business_id)
    
    def get_all_profiles(self):
        """Get all business profiles"""
        return list(self.profiles.values())