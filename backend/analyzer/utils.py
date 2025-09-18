from rest_framework.response import Response
import requests 
import json
import re
import os
from time import sleep
from dotenv import load_dotenv
load_dotenv()

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
# API_KEY = "AIzaSyDsy83ifKNQZaXnhRhitFYdET6xmSGhGss"
API_KEY = os.getenv("GEMINI_API_KEY")
HEADERS = {"Content-Type": "application/json"}
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

if not API_KEY:
    raise ValueError("❌ No GEMINI_API_KEY found. Set it in .env or environment variables.")

def call_gemini(prompt):
    params = {"key": API_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        ],
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=data, params=params, timeout=30)
            response.raise_for_status()

            result = response.json()

            # ✅ Parse response correctly
            if result and "candidates" in result and result["candidates"]:
                first_candidate = result["candidates"][0]
                if (
                    "content" in first_candidate
                    and "parts" in first_candidate["content"]
                    and first_candidate["content"]["parts"]
                ):
                    first_part = first_candidate["content"]["parts"][0]
                    if "text" in first_part:
                        full_text_response = first_part["text"]

                        # Extract JSON if wrapped in ```json ... ```
                        json_match = re.search(r"```json\n(.*?)```", full_text_response, re.DOTALL)
                        if json_match:
                            return json_match.group(1)  # ✅ return as string
                        return full_text_response.strip()

            raise Exception(f"Unexpected Gemini API response structure: {result}")

        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES:
                sleep(RETRY_DELAY)
                continue
            raise Exception("Gemini API timeout, please retry.")
        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES:
                print(f"[Attempt {attempt}] Network/API error: {e}")
                sleep(RETRY_DELAY)
                continue
            raise Exception(f"Gemini API unreachable after {MAX_RETRIES} attempts: {e}")
def extract_skill_and_recommendations(resume_text):
    prompt = f"""
You are an AI career advisor. Analyze the following resume text.

1. Extract all technical and soft skills. Return them as a JSON array.
2. Suggest the top 5 most relevant career paths. For each career include:
   - career name
   - match_score (0–100)
   - present_skills
   - missing_skills
   - at least 3 learning resources (with name, link, and free True/False)

Return ONLY valid JSON in the following format:

{{
  "skills": ["skill1", "skill2", "skill3"],
  "recommendations": [
    {{
      "career": "Career Name",
      "match_score": 75.0,
      "present_skills": ["skill1", "skill2"],
      "missing_skills": ["skill3"],
      "resources": [
        {{"name": "Resource name","link": "https://example.com","free": "True/False"}}
      ]
    }}
  ]
}}

Resume text: {resume_text}
"""

    response_json_str = call_gemini(prompt)  # ✅ plain string now

    try:
        return json.loads(response_json_str)  # ✅ works now
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from Gemini: {e}\nResponse was:\n{response_json_str}")
        raise Exception("Failed to parse response JSON.")
