from pydantic import BaseModel, Field
from typing import Optional

class AnalysisRequest(BaseModel):
    user_text: str = Field(..., alias="User_Text", description="The content the user wants to post.")
    registered_domain: str = Field(..., alias="Registered_Domain", description="The verified industry category of the startup.")
    business_id: Optional[str] = Field(None, alias="Business_ID", description="Optional business ID for domain-specific enforcement.")

    class Config:
        populate_by_name = True

class AnalysisResponse(BaseModel):
    status: str = Field(..., description="Approved / Rejected / Flagged for Manual Review")
    reason: str = Field(..., description="Brief explanation of why it was blocked or allowed")
    confidence_score: float = Field(..., description="Confidence score between 0.0 and 1.0")
    detected_category: str = Field(..., description="The industry sector detected in the text")
