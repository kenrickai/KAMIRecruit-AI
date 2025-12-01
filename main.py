import os
import pkg_resources
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# --------------------------
# TEMP DEBUG LOGGING (REMOVE LATER)
# --------------------------
print(">>> DEBUG: Starting server...")
raw_key = os.getenv("GEMINI_API_KEY")

print(">>> DEBUG: GEMINI_API_KEY exists:", raw_key is not None)
if raw_key:
    print(">>> DEBUG: GEMINI_API_KEY length:", len(raw_key))
    print(">>> DEBUG: GEMINI_API_KEY starts with:", raw_key[:10])
else:
    print(">>> DEBUG: GEMINI_API_KEY IS MISSING!")

# --------------------------
# Configure Gemini API
# --------------------------
if raw_key:
    genai.configure(api_key=raw_key)
else:
    print(">>> ERROR: No API key loaded. Gemini will fail!")

MODEL_NAME = "models/gemini-1.5-flash"
print(">>> USING MODEL:", MODEL_NAME)


# --------------------------
# FastAPI App Setup
# --------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Request Body Schema
# --------------------------
class ChatRequest(BaseModel):
    message: str


# --------------------------
# Chat Endpoint
# --------------------------
@app.post("/api/chat")
async def chat_api(req: ChatRequest):
    try:
        response = genai.generate_text(
            model=MODEL_NAME,
            prompt=req.message
        )
        return {"reply": response.result}

    except Exception as e:
        print(">>> ERROR during model call:", str(e))
        return {"reply": f"⚠️ Error: {str(e)}"}


# --------------------------
# Root Endpoint
# --------------------------
@app.get("/")
def home():
    return {"status": "Backend is running", "model": MODEL_NAME}
