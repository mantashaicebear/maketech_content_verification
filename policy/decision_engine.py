"""
Decision Engine for Content Verification - Updated for Marketplace
"""

import json
import os
from typing import Dict

class DecisionEngine:
    """Decision engine for business rules - Updated for marketplace"""
    
    def __init__(self):
        self.restricted_categories = [
            'weapons', 'drugs', 'adult_content', 'gambling',
            'explosives', 'prescription_medicine', 'counterfeit',
            'human_organs', 'wildlife', 'harmful_chemicals'
        ]
        
        self.business_domains = [
            'food', 'tech', 'education', 'health', 'finance',
            'fashion', 'electronics', 'automotive', 'real_estate',
            'entertainment', 'travel', 'beauty', 'home', 'sports',
            'other'
        ]
    
    def make_decision(self, content_prediction: Dict, business_profile: Dict = None) -> Dict:
        """Make decision based on content and business rules - Updated for marketplace"""
        try:
            predicted_category = content_prediction.get('category', 'unknown')
            confidence = content_prediction.get('confidence', 0.0)
            is_restricted = content_prediction.get('is_restricted', False)
            
            # Default decision
            decision = {
                'is_allowed': True,
                'decision': 'approved',
                'reason': 'Content verified successfully',
                'warning_message': '',
                'requires_review': False,
                'severity': 'low'
            }
            
            # Check 1: Restricted categories (blocks all businesses)
            if is_restricted or predicted_category in self.restricted_categories:
                decision['is_allowed'] = False
                decision['decision'] = 'blocked'
                decision['reason'] = f'Content falls under restricted category: {predicted_category}'
                decision['warning_message'] = self._get_warning_message(predicted_category)
                decision['severity'] = 'high'
                return decision
            
            # Check 2: Very low confidence (below 0.3)
            if confidence < 0.3:
                decision['requires_review'] = True
                decision['reason'] = f'Very low prediction confidence: {confidence:.2f}'
                decision['warning_message'] = 'Content classification uncertain. Requires manual review.'
                decision['severity'] = 'medium'
                decision['is_allowed'] = False
            # Check 3: Low confidence (0.3-0.5) - warning but might allow
            elif confidence < 0.5:
                decision['requires_review'] = False
                decision['reason'] = f'Moderate prediction confidence: {confidence:.2f}'
                decision['warning_message'] = 'Content classification has moderate confidence.'
                decision['severity'] = 'low'
            
            # Check 4: Business-specific rules (only if confidence >= 0.3)
            if business_profile and confidence >= 0.3:
                business_type = business_profile.get('business_type', 'single_domain')
                business_domain = business_profile.get('business_domain', '')
                allowed_domains = business_profile.get('allowed_domains', [])
                
                if business_type == 'single_domain':
                    if predicted_category != business_domain and predicted_category != 'unknown':
                        decision['is_allowed'] = False
                        decision['decision'] = 'blocked'
                        decision['reason'] = f'Content category "{predicted_category}" does not match business domain "{business_domain}"'
                        decision['warning_message'] = f'Your business is registered for "{business_domain}" domain. Please post only domain-specific content.'
                        decision['severity'] = 'medium'
                
                elif business_type == 'marketplace':
                    if allowed_domains:
                        if predicted_category in allowed_domains:
                            # Category is allowed for this marketplace
                            decision['is_allowed'] = True
                            decision['decision'] = 'approved'
                            decision['reason'] = f'Content category "{predicted_category}" is allowed for this marketplace'
                            decision['severity'] = 'low'
                        elif predicted_category != 'unknown':
                            # Category not in allowed domains - needs review
                            decision['requires_review'] = True
                            decision['is_allowed'] = False
                            decision['decision'] = 'needs_review'
                            decision['reason'] = f'Content category "{predicted_category}" is not in allowed domains for this marketplace'
                            decision['warning_message'] = f'Content about "{predicted_category}" requires review for marketplace listing.'
                            decision['severity'] = 'low'
            
            # Check 5: Unknown category with reasonable confidence
            if predicted_category == 'unknown' and confidence >= 0.3:
                decision['requires_review'] = True
                decision['is_allowed'] = False
                decision['reason'] = 'Content could not be classified into a specific category'
                decision['warning_message'] = 'Unable to determine content category. Requires manual review.'
                decision['severity'] = 'medium'
            
            # Final decision logic
            if decision['requires_review']:
                decision['decision'] = 'needs_review'
                decision['is_allowed'] = False
            
            return decision
            
        except Exception as e:
            return {
                'is_allowed': False,
                'decision': 'error',
                'reason': f'Decision error: {str(e)}',
                'warning_message': 'System error occurred during verification.',
                'requires_review': True,
                'severity': 'critical'
            }
    
    def _get_warning_message(self, category: str) -> str:
        """Get warning message for restricted category"""
        warnings = {
            'weapons': 'This content is related to Weapons and Firearms, which violates our marketplace safety policy.',
            'drugs': 'This content is related to Drugs and Narcotics, which is prohibited on our platform.',
            'adult_content': 'Adult content is not allowed on our business platform.',
            'gambling': 'Gambling-related content is restricted in many jurisdictions and not allowed.',
            'counterfeit': 'Counterfeit goods are illegal and strictly prohibited.',
            'prescription_medicine': 'Selling prescription medicines requires special licenses and is restricted.',
            'harmful_chemicals': 'Harmful chemicals require special licenses and safety certifications.'
        }
        return warnings.get(category, 'This content violates our platform policies.')
    
    def get_restricted_categories(self):
        """Get restricted categories"""
        return self.restricted_categories
    
    def get_business_domains(self):
        """Get business domains"""
        return self.business_domains