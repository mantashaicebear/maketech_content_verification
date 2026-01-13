import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def analyze_content(user_text: str, registered_domain: str) -> dict:
    if not API_KEY:
        raise ValueError("Gemini API Key is missing in environment variables.")

    model = genai.GenerativeModel('gemini-flash-latest')

    prompt = f"""
    Role: You are the "Venture Content Guard," a high-precision content moderation AI for a professional startup platform.

    Core Objective: Your job is to analyze incoming text posts from businesses and verify two things:
    1. Does the content strictly belong to the business's registered Industry Domain?
    2. Is the content Professional and Related to business growth (No spam, no personal rants, no off-topic memes)?

    Input Data Provided:
    User_Text: "{user_text}"
    Registered_Domain: "{registered_domain}"

    Verification Logic:
    STEP 1 (Professionalism Check): Scan for "Unrelated Content." If the text contains political debates, personal social life updates, or aggressive non-business language, label it [REJECTED: OFF-TOPIC].
    STEP 2 (Domain Alignment): Compare the User_Text context to the Registered_Domain.

    Output Format (JSON):
    You must return exactly this JSON structure:
    {{
     "status": "Approved / Rejected: Reason",
     "reason": "Brief explanation of why it was blocked or allowed",
     "confidence_score": "0.0 to 1.0 (float)",
     "detected_category": "The industry sector you detected in the text"
    }}

    Constraint: If the confidence_score is below 0.80, mark the status as "Flagged for Manual Review".
    Ensure the response is valid JSON.
    """

    try:
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        # Clean up code blocks
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "").replace("```", "").strip()
        elif text_response.startswith("```"):
             text_response = text_response.replace("```", "").strip()
        
        data = json.loads(text_response)
        
        # Logic check for confidence
        try:
            conf = float(data.get("confidence_score", 0.0))
            if conf < 0.80:
                data["status"] = "Flagged for Manual Review"
        except ValueError:
            pass # Keep original status if score isn't a float
            
        return data
        
    except Exception as e:
        # Re-raise the exception to be handled by the API layer
        raise RuntimeError(f"Gemini API Error: {str(e)}")
