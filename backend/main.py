from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Allow Chrome extension to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    text: str
    tone: str = "professional"

GEMINI_API_KEY = ""


GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

@app.get("/")
def read_root():
    return {"status": "LinkedIn Post Generator API Running"}

@app.get("/list-models")
def list_available_models():
    """
    Check what models are available with your API key
    """
    try:
        # Try v1 (stable)
        res = requests.get(
            f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}",
            timeout=10
        )
        
        if res.status_code == 200:
            models = res.json()
            available = [m.get('name', 'unknown') for m in models.get('models', [])]
            return {
                "api_version": "v1",
                "status": "success",
                "available_models": available
            }
        
        # If v1 fails, try v1beta
        res_beta = requests.get(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}",
            timeout=10
        )
        
        if res_beta.status_code == 200:
            models = res_beta.json()
            available = [m.get('name', 'unknown') for m in models.get('models', [])]
            return {
                "api_version": "v1beta",
                "status": "success",
                "available_models": available
            }
        
        return {
            "status": "error",
            "message": f"v1: {res.status_code}, v1beta: {res_beta.status_code}",
            "v1_response": res.text[:500],
            "v1beta_response": res_beta.text[:500]
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/generate")
def generate_post(prompt: Prompt):
    """
    Generate a LinkedIn post from user input
    """
    
    enhanced_prompt = f"""Create a professional LinkedIn post about: {prompt.text}

Requirements:
- Tone: {prompt.tone}
- Length: 150-200 words
- Include relevant emojis (2-3 maximum)
- Add 3-5 relevant hashtags at the end
- Make it engaging and valuable
- Use line breaks for readability

Write the post now:"""
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": enhanced_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500,
        }
    }

    # Try multiple model names and API versions
    urls_to_try = [
        # v1 (stable) - Gemini 2.x models (your available models)
        "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent",
    ]

    last_error = None
    
    for url in urls_to_try:
        try:
            print(f"\n🔄 Trying: {url}")
            
            res = requests.post(
                f"{url}?key={GEMINI_API_KEY}",
                json=payload,
                timeout=30
            )
            
            print(f"Status Code: {res.status_code}")
            
            if res.status_code == 200:
                data = res.json()
                output = data["candidates"][0]["content"]["parts"][0]["text"]
                
                print(f"✅ SUCCESS with {url}")
                
                return {
                    "success": True,
                    "response": output,
                    "model_used": url.split("/models/")[1].split(":")[0]
                }
            else:
                print(f"❌ Failed: {res.text[:200]}")
                last_error = res.text
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            last_error = str(e)
            continue
    
    # If all attempts failed
    return {
        "success": False,
        "response": "Could not generate post. Please check API key or try /list-models endpoint.",
        "error": last_error,
        "suggestion": "Visit http://localhost:8000/list-models to see available models"
    }

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting server...")
    print("📋 Visit http://localhost:8000/list-models to see available models")
    print("🧪 Visit http://localhost:8000/docs for API documentation\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)