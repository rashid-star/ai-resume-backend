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
You are an expert ATS resume analyzer and career advisor.

Analyze the resume and return ONLY valid JSON.

Resume:
{resume_text}

Tasks:
1. Evaluate resume quality and ATS compatibility.
2. Predict the best career role based on skills and experience.
3. Identify strengths found in the resume.
4. Identify missing skills required for the predicted role.
5. Suggest improvements to strengthen the resume.

Return JSON exactly in this format:

{{
 "resume_score": number,
 "ats_score": number,
 "best_role": "string",
 "domain": "string",
 "strengths": ["skill1","skill2"],
 "missing_skills": ["skill1","skill2"],
 "improvements": ["improvement1","improvement2"],
 "summary": "2-3 sentence professional summary"
}}

Rules:
- resume_score must be between 0 and 100
- ats_score must be between 0 and 100
- domain examples: Artificial Intelligence, Data Science, Web Development, DevOps, Software Engineering
- Missing skills must depend on the predicted best_role
- Summary must be concise (2-3 sentences)
- Return STRICT JSON only
"""

    try:

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )

        result = response.choices[0].message.content.strip()

        # Remove markdown formatting if present
        cleaned = re.sub(r"```json|```", "", result).strip()

        # Extract JSON block
        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in AI response")

        json_text = json_match.group()

        data = json.loads(json_text)

        return {
            "resume_score": data.get("resume_score", 0),
            "ats_score": data.get("ats_score", 0),
            "best_role": data.get("best_role", "N/A"),
            "domain": data.get("domain", "General"),
            "missing_skills": data.get("missing_skills", []),
            "strengths": data.get("strengths", []),
            "improvements": data.get("improvements", []),
            "summary": data.get("summary", "No summary available")
        }

    except Exception as e:
        print("Groq AI Error:", e)

        # Safe fallback response
        return {
            "resume_score": 0,
            "ats_score": 0,
            "best_role": "N/A",
            "domain": "Unknown",
            "missing_skills": [],
            "strengths": [],
            "improvements": [],
            "summary": "AI analysis failed"
        }