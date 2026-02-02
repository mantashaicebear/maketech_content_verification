from fastapi import FastAPI, HTTPException
from app.models import AnalysisRequest, AnalysisResponse
from app.trained_model_analyzer import analyze_content
import uvicorn

app = FastAPI(
    title="Venture Content Guard",
    description="A high-precision content moderation API for a professional startup platform.",
    version="1.0.0"
)

@app.post("/analyze", response_model=AnalysisResponse, status_code=200)
async def analyze_post(request: AnalysisRequest):
    """
    Analyze incoming text posts for domain alignment and professionalism.
    """
    try:
        result = analyze_content(request.user_text, request.registered_domain, request.business_id)
        return result
        
    except ValueError as e:
        # Configuration error (e.g. missing API key)
        raise HTTPException(status_code=500, detail=str(e))
        
    except RuntimeError as e:
        # External service error (Gemini API failed, Quota exceeded, etc.)
        # 503 Service Unavailable is appropriate for upstream failures
        raise HTTPException(status_code=503, detail=str(e))
        
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
