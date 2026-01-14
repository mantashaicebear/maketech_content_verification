"""
Decision Engine for Content Verification
Applies business rules to predictions
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Any, Optional

logger = logging.getLogger(__name__)

class DecisionEngine:
    """
    Decision engine for content verification
    """
    
    def __init__(self, policy_path: str = None):
        """
        Initialize decision engine
        
        Args:
            policy_path: Path to policy configuration
        """
        self.policy_path = policy_path or "policy/restricted_categories.json"
        self.policies = self._load_policies()
        
        # Business types
        self.business_types = {
            'single_domain': 'Single Domain Business',
            'marketplace': 'Marketplace Business',
            'multi_domain': 'Multi-Domain Business'
        }
        
        # Severity levels
        self.severity_levels = {
            'low': {'action': 'warn', 'message': 'Content may not be optimal'},
            'medium': {'action': 'review', 'message': 'Content requires review'},
            'high': {'action': 'block', 'message': 'Content violates policies'},
            'critical': {'action': 'block+report', 'message': 'Severe policy violation'}
        }
        
        logger.info("DecisionEngine initialized")
    
    def _load_policies(self) -> Dict:
        """Load policies from file"""
        default_policies = {
            "restricted_categories": [
                "weapons", "explosives", "drugs", "prescription_medicine",
                "alcohol", "tobacco", "counterfeit", "human_organs",
                "wildlife", "harmful_chemicals", "surveillance",
                "hacking_tools", "gambling", "adult_content",
                "hate_speech", "pyramid_schemes", "illegal_services"
            ],
            "high_risk_categories": [
                "weapons", "drugs", "adult_content", "counterfeit"
            ],
            "medium_risk_categories": [
                "prescription_medicine", "alcohol", "tobacco",
                "surveillance", "gambling"
            ],
            "business_domains": [
                "food", "tech", "education", "healthcare", "finance",
                "fashion", "electronics", "automotive", "real_estate",
                "entertainment", "sports", "travel", "beauty", "home"
            ],
            "rules": {
                "single_domain_business": {
                    "description": "Must post only in registered domain",
                    "action": "strict"
                },
                "marketplace_business": {
                    "description": "Can post in multiple domains but not restricted categories",
                    "action": "flexible"
                }
            }
        }
        
        try:
            if os.path.exists(self.policy_path):
                with open(self.policy_path, 'r') as f:
                    policies = json.load(f)
                default_policies.update(policies)
                logger.info(f"Policies loaded from {self.policy_path}")
        except Exception as e:
            logger.error(f"Error loading policies: {e}")
        
        return default_policies
    
    def make_decision(
        self,
        content_prediction: Dict,
        business_profile: Dict
    ) -> Dict:
        """
        Make decision based on content prediction and business profile
        
        Args:
            content_prediction: Prediction result from classifiers
            business_profile: Business profile information
            
        Returns:
            Decision result
        """
        try:
            # Extract information
            predicted_category = content_prediction.get('category', 'unknown')
            confidence = content_prediction.get('confidence', 0.0)
            is_restricted = content_prediction.get('is_restricted', False)
            
            business_type = business_profile.get('business_type', 'single_domain')
            business_domain = business_profile.get('business_domain', '')
            allowed_domains = business_profile.get('allowed_domains', [])
            
            # Initialize decision
            decision = {
                'is_allowed': False,
                'decision': 'pending',
                'reason': '',
                'severity': 'low',
                'requires_review': False,
                'warning_message': '',
                'suggested_action': 'none'
            }
            
            # Check 1: Restricted categories (applies to all businesses)
            if is_restricted:
                decision['is_allowed'] = False
                decision['decision'] = 'blocked'
                decision['reason'] = f'Content falls under restricted category: {predicted_category}'
                decision['severity'] = self._get_severity_level(predicted_category)
                decision['warning_message'] = self._get_warning_message(predicted_category)
                decision['suggested_action'] = 'block'
                return decision
            
            # Check 2: Low confidence
            if confidence < 0.3:
                decision['requires_review'] = True
                decision['reason'] = f'Low prediction confidence: {confidence:.2f}'
                decision['severity'] = 'medium'
                decision['warning_message'] = 'Content classification uncertain. Requires manual review.'
                decision['suggested_action'] = 'review'
            
            # Check 3: Business-specific rules
            if business_type == 'single_domain':
                # Single domain business - must match registered domain
                if predicted_category != business_domain and predicted_category != 'unknown':
                    decision['is_allowed'] = False
                    decision['decision'] = 'domain_mismatch'
                    decision['reason'] = f'Content category "{predicted_category}" does not match business domain "{business_domain}"'
                    decision['severity'] = 'medium'
                    decision['warning_message'] = f'Your business is registered for "{business_domain}" domain. Please post only domain-specific content.'
                    decision['suggested_action'] = 'block'
                else:
                    decision['is_allowed'] = True
                    decision['decision'] = 'approved'
                    decision['reason'] = 'Content matches business domain'
                    
            elif business_type == 'marketplace':
                # Marketplace business - check if in allowed domains
                if allowed_domains and predicted_category not in allowed_domains and predicted_category != 'unknown':
                    decision['requires_review'] = True
                    decision['reason'] = f'Content category "{predicted_category}" is not in allowed domains'
                    decision['severity'] = 'low'
                    decision['warning_message'] = f'Content about "{predicted_category}" requires review for marketplace listing.'
                    decision['suggested_action'] = 'review'
                else:
                    decision['is_allowed'] = True
                    decision['decision'] = 'approved'
                    decision['reason'] = 'Content allowed for marketplace'
                    
            else:
                # Multi-domain or unknown business type
                decision['is_allowed'] = True
                decision['decision'] = 'approved'
                decision['reason'] = 'Content approved for multi-domain business'
            
            # Check 4: Borderline cases
            if 0.3 <= confidence <= 0.6:  # Borderline confidence
                decision['requires_review'] = True
                decision['reason'] = f'Borderline confidence ({confidence:.2f}) for category "{predicted_category}"'
                decision['warning_message'] = 'Content classification is uncertain. Requires manual verification.'
                decision['suggested_action'] = 'review'
            
            # Final decision logic
            if decision['is_allowed'] and decision['requires_review']:
                decision['decision'] = 'needs_review'
                decision['is_allowed'] = False  # Don't allow until reviewed
            
            logger.info(f"Decision: {decision['decision']} - {decision['reason']}")
            
            return decision
            
        except Exception as e:
            logger.error(f"Error in decision making: {e}")
            return {
                'is_allowed': False,
                'decision': 'error',
                'reason': f'Decision error: {str(e)}',
                'severity': 'critical',
                'requires_review': True,
                'warning_message': 'System error occurred during verification.',
                'suggested_action': 'review'
            }
    
    def _get_severity_level(self, category: str) -> str:
        """Get severity level for a category"""
        if category in self.policies.get('high_risk_categories', []):
            return 'critical'
        elif category in self.policies.get('medium_risk_categories', []):
            return 'high'
        elif category in self.policies.get('restricted_categories', []):
            return 'medium'
        else:
            return 'low'
    
    def _get_warning_message(self, category: str) -> str:
        """Get warning message for a restricted category"""
        warnings = {
            'weapons': 'This content is related to Weapons and Firearms, which violates our marketplace safety policy.',
            'drugs': 'This content is related to Drugs and Narcotics, which is prohibited on our platform.',
            'adult_content': 'Adult content is not allowed on our business platform.',
            'counterfeit': 'Counterfeit goods are illegal and strictly prohibited.',
            'prescription_medicine': 'Selling prescription medicines requires special licenses and is restricted.',
            'harmful_chemicals': 'Harmful chemicals require special licenses and safety certifications.',
            'surveillance': 'Surveillance devices may violate privacy laws.',
            'gambling': 'Gambling-related content is restricted in many jurisdictions.',
            'hate_speech': 'Hate speech content violates our community guidelines.',
            'wildlife': 'Trade of protected wildlife is illegal and violates conservation laws.'
        }
        
        return warnings.get(category, 'This content violates our platform policies.')
    
    def get_restricted_categories(self) -> List[str]:
        """Get list of restricted categories"""
        return self.policies.get('restricted_categories', [])
    
    def get_business_domains(self) -> List[str]:
        """Get list of business domains"""
        return self.policies.get('business_domains', [])
    
    def add_restricted_category(self, category: str, severity: str = 'medium'):
        """Add a new restricted category"""
        if category not in self.policies['restricted_categories']:
            self.policies['restricted_categories'].append(category)
            
            # Update severity mapping
            if severity == 'high':
                if 'high_risk_categories' not in self.policies:
                    self.policies['high_risk_categories'] = []
                self.policies['high_risk_categories'].append(category)
            elif severity == 'medium':
                if 'medium_risk_categories' not in self.policies:
                    self.policies['medium_risk_categories'] = []
                self.policies['medium_risk_categories'].append(category)
            
            self._save_policies()
            logger.info(f"Added restricted category: {category}")
    
    def _save_policies(self):
        """Save policies to file"""
        try:
            os.makedirs(os.path.dirname(self.policy_path), exist_ok=True)
            with open(self.policy_path, 'w') as f:
                json.dump(self.policies, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving policies: {e}")