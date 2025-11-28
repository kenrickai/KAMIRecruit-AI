# models_test.py
# Test Gemini model availability

import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("\n=== AVAILABLE GEMINI MODELS ===\n")

models = client.models.list()

for m in models:
    print(m.name)
