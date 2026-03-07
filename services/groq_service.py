# ============================================
# GROQ AI SERVICE
# Handles resume analysis using LLM (Groq)
# ============================================

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_resume_with_ai(resume_text: str):
    """
    Sends resume text to Groq LLM and returns structured JSON analysis.
    """

    prompt = f"""
You are a professional ATS resume analyzer.

Analyze the resume and return ONLY valid JSON.

Resume:
{resume_text}

Return JSON exactly like this:

{{
 "resume_score": number,
 "ats_score": number,
 "best_role": "string",
 "missing_skills": ["skill1","skill2"],
 "strengths": ["strength1","strength2"],
 "improvements": ["improvement1","improvement2"],
 "summary": "short summary"
}}

Rules:
- resume_score out of 100
- ats_score out of 100
- Return STRICT JSON
- No explanation
"""

    try:

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )

        result = response.choices[0].message.content.strip()

        # Remove markdown if present
        cleaned = re.sub(r"```json|```", "", result).strip()

        # Extract JSON block if model added extra text
        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in AI response")

        json_text = json_match.group()

        data = json.loads(json_text)

        return {
            "resume_score": data.get("resume_score", 0),
            "ats_score": data.get("ats_score", 0),
            "best_role": data.get("best_role", "N/A"),
            "missing_skills": data.get("missing_skills", []),
            "strengths": data.get("strengths", []),
            "improvements": data.get("improvements", []),
            "summary": data.get("summary", "No summary available")
        }

    except Exception as e:
        print("Groq AI Error:", e)

        # Always return safe structure
        return {
            "resume_score": 0,
            "ats_score": 0,
            "best_role": "N/A",
            "missing_skills": [],
            "strengths": [],
            "improvements": [],
            "summary": "AI analysis failed"
        }