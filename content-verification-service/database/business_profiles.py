"""
Business Profile Database Module
Manages business profile data
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class BusinessProfileDB:
    """
    Business profile database (file-based for demo)
    In production, replace with actual database
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize business profile database
        
        Args:
            db_path: Path to database file
        """
        self.db_path = db_path or "database/business_profiles.json"
        self.profiles = self._load_profiles()
        
        logger.info(f"BusinessProfileDB initialized with {len(self.profiles)} profiles")
    
    def _load_profiles(self) -> Dict[str, Dict]:
        """Load profiles from file"""
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
                "owner_id": "U001",
                "created_at": "2024-01-01"
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
                "owner_id": "U002",
                "created_at": "2024-01-05"
            },
            "B003": {
                "id": "B003",
                "business_name": "Marketplace Hub",
                "business_type": "marketplace",
                "business_domain": "multi",
                "allowed_domains": ["tech", "fashion", "electronics", "home"],
                "is_verified": True,
                "verification_date": "2024-01-25",
                "registration_number": "MKT001",
                "owner_id": "U003",
                "created_at": "2024-01-10"
            }
        }
        
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    profiles = json.load(f)
                # Merge with defaults
                default_profiles.update(profiles)
                logger.info(f"Profiles loaded from {self.db_path}")
        except Exception as e:
            logger.error(f"Error loading profiles: {e}")
        
        return default_profiles
    
    def get_profile(self, business_id: str) -> Optional[Dict]:
        """
        Get business profile by ID
        
        Args:
            business_id: Business ID
            
        Returns:
            Business profile or None
        """
        return self.profiles.get(business_id)
    
    def get_profiles_by_owner(self, owner_id: str) -> List[Dict]:
        """
        Get all business profiles for an owner
        
        Args:
            owner_id: Owner user ID
            
        Returns:
            List of business profiles
        """
        return [
            profile for profile in self.profiles.values()
            if profile.get('owner_id') == owner_id
        ]
    
    def create_profile(self, profile_data: Dict) -> Optional[Dict]:
        """
        Create new business profile
        
        Args:
            profile_data: Profile data
            
        Returns:
            Created profile or None
        """
        try:
            business_id = profile_data.get('id')
            if not business_id:
                # Generate new ID
                business_id = f"B{len(self.profiles) + 1:03d}"
                profile_data['id'] = business_id
            
            # Validate required fields
            required_fields = ['business_name', 'business_type', 'business_domain']
            for field in required_fields:
                if field not in profile_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Set default values
            profile_data.setdefault('is_verified', False)
            profile_data.setdefault('allowed_domains', [profile_data['business_domain']])
            profile_data.setdefault('created_at', '2024-01-01')
            
            # Add to profiles
            self.profiles[business_id] = profile_data
            
            # Save to file
            self._save_profiles()
            
            logger.info(f"Created profile for {profile_data['business_name']} (ID: {business_id})")
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error creating profile: {e}")
            return None
    
    def update_profile(self, business_id: str, updates: Dict) -> Optional[Dict]:
        """
        Update business profile
        
        Args:
            business_id: Business ID
            updates: Fields to update
            
        Returns:
            Updated profile or None
        """
        try:
            if business_id not in self.profiles:
                logger.error(f"Profile not found: {business_id}")
                return None
            
            # Update fields
            for key, value in updates.items():
                self.profiles[business_id][key] = value
            
            # Save to file
            self._save_profiles()
            
            logger.info(f"Updated profile: {business_id}")
            
            return self.profiles[business_id]
            
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            return None
    
    def delete_profile(self, business_id: str) -> bool:
        """
        Delete business profile
        
        Args:
            business_id: Business ID
            
        Returns:
            Success status
        """
        try:
            if business_id in self.profiles:
                del self.profiles[business_id]
                self._save_profiles()
                logger.info(f"Deleted profile: {business_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            return False
    
    def search_profiles(self, query: str) -> List[Dict]:
        """
        Search business profiles
        
        Args:
            query: Search query
            
        Returns:
            List of matching profiles
        """
        results = []
        query_lower = query.lower()
        
        for profile in self.profiles.values():
            # Search in name and domain
            if (query_lower in profile.get('business_name', '').lower() or
                query_lower in profile.get('business_domain', '').lower() or
                query_lower in ' '.join(profile.get('allowed_domains', [])).lower()):
                results.append(profile)
        
        return results
    
    def _save_profiles(self):
        """Save profiles to file"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with open(self.db_path, 'w') as f:
                json.dump(self.profiles, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving profiles: {e}")
    
    def get_all_profiles(self) -> List[Dict]:
        """Get all business profiles"""
        return list(self.profiles.values())
    
    def verify_business(self, business_id: str) -> bool:
        """
        Verify a business
        
        Args:
            business_id: Business ID
            
        Returns:
            Success status
        """
        try:
            if business_id in self.profiles:
                self.profiles[business_id]['is_verified'] = True
                self._save_profiles()
                logger.info(f"Verified business: {business_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error verifying business: {e}")
            return False