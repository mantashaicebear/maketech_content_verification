"""
Content Verification Service - Main Entry Point
Handles both text and image content verification
"""

import os
import sys
import json
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

from api.verify_content import ContentVerificationAPI
from database.business_profiles import BusinessProfileDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Content Verification Service",
    description="AI-powered content verification for businesses",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
content_api = ContentVerificationAPI()
business_db = BusinessProfileDB()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Content Verification Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "/verify/text": "Verify text content",
            "/verify/image": "Verify image content",
            "/verify/mixed": "Verify mixed content (text + images)",
            "/verify/business": "Verify content for specific business",
            "/business/{business_id}": "Get business profile",
            "/categories": "Get available categories",
            "/restricted": "Get restricted categories"
        }
    }

@app.post("/verify/text")
async def verify_text(
    text: str = Form(...),
    title: str = Form(""),
    business_id: Optional[str] = Form(None)
):
    """
    Verify text content
    
    Args:
        text: Content text
        title: Content title (optional)
        business_id: Business ID for context-aware verification
    
    Returns:
        Verification result
    """
    try:
        logger.info(f"Verifying text content: {title[:50]}...")
        
        # Get business profile if provided
        business_profile = None
        if business_id:
            business_profile = business_db.get_profile(business_id)
        
        # Verify content
        result = content_api.verify_text(
            text=text,
            title=title,
            business_profile=business_profile
        )
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error verifying text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify/image")
async def verify_image(
    image: UploadFile = File(...),
    business_id: Optional[str] = Form(None)
):
    """
    Verify image content
    
    Args:
        image: Image file
        business_id: Business ID for context-aware verification
    
    Returns:
        Verification result
    """
    try:
        logger.info(f"Verifying image: {image.filename}")
        
        # Save uploaded image temporarily
        temp_path = f"/tmp/{image.filename}"
        with open(temp_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        
        # Get business profile if provided
        business_profile = None
        if business_id:
            business_profile = business_db.get_profile(business_id)
        
        # Verify content
        result = content_api.verify_image(
            image_path=temp_path,
            business_profile=business_profile
        )
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except:
            pass
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error verifying image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify/mixed")
async def verify_mixed(
    text: str = Form(...),
    title: str = Form(""),
    images: List[UploadFile] = File(...),
    business_id: Optional[str] = Form(None)
):
    """
    Verify mixed content (text + images)
    
    Args:
        text: Content text
        title: Content title (optional)
        images: List of image files
        business_id: Business ID for context-aware verification
    
    Returns:
        Verification result
    """
    try:
        logger.info(f"Verifying mixed content with {len(images)} images")
        
        # Save uploaded images temporarily
        temp_paths = []
        for image in images:
            temp_path = f"/tmp/{image.filename}"
            with open(temp_path, "wb") as buffer:
                content = await image.read()
                buffer.write(content)
            temp_paths.append(temp_path)
        
        # Get business profile if provided
        business_profile = None
        if business_id:
            business_profile = business_db.get_profile(business_id)
        
        # Verify content
        result = content_api.verify_mixed(
            text=text,
            title=title,
            image_paths=temp_paths,
            business_profile=business_profile
        )
        
        # Clean up temp files
        for temp_path in temp_paths:
            try:
                os.remove(temp_path)
            except:
                pass
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error verifying mixed content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify/business")
async def verify_for_business(
    text: str = Form(""),
    title: str = Form(""),
    business_id: str = Form(...),
    images: Optional[List[UploadFile]] = File(None)
):
    """
    Verify content for a specific business
    
    Args:
        text: Content text
        title: Content title (optional)
        business_id: Business ID (required)
        images: List of image files (optional)
    
    Returns:
        Verification result with business-specific rules
    """
    try:
        logger.info(f"Verifying content for business: {business_id}")
        
        # Get business profile
        business_profile = business_db.get_profile(business_id)
        if not business_profile:
            raise HTTPException(status_code=404, detail="Business not found")
        
        # Save uploaded images temporarily if provided
        temp_paths = []
        if images:
            for image in images:
                temp_path = f"/tmp/{image.filename}"
                with open(temp_path, "wb") as buffer:
                    content = await image.read()
                    buffer.write(content)
                temp_paths.append(temp_path)
        
        # Verify content
        result = content_api.verify_for_business(
            text=text,
            title=title,
            image_paths=temp_paths,
            business_profile=business_profile
        )
        
        # Clean up temp files
        for temp_path in temp_paths:
            try:
                os.remove(temp_path)
            except:
                pass
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error verifying for business: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/business/{business_id}")
async def get_business(business_id: str):
    """
    Get business profile
    
    Args:
        business_id: Business ID
    
    Returns:
        Business profile information
    """
    try:
        profile = business_db.get_profile(business_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Business not found")
        
        return {
            "success": True,
            "data": profile
        }
        
    except Exception as e:
        logger.error(f"Error getting business: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories")
async def get_categories():
    """
    Get all available categories
    
    Returns:
        List of categories
    """
    try:
        categories = content_api.get_categories()
        return {
            "success": True,
            "data": categories
        }
        
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restricted")
async def get_restricted_categories():
    """
    Get restricted categories
    
    Returns:
        List of restricted categories
    """
    try:
        restricted = content_api.get_restricted_categories()
        return {
            "success": True,
            "data": restricted
        }
        
    except Exception as e:
        logger.error(f"Error getting restricted categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "content-verification",
        "timestamp": datetime.now().isoformat()
    }

def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI server"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    # Run the server
    run_server()


