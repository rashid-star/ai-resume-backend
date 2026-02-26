# ============================================
# GROQ AI SERVICE
# Handles resume analysis using LLM (Groq)
# ============================================

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables (.env file)
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_resume_with_ai(resume_text: str):
    """
    Sends resume text to Groq LLM and returns structured JSON analysis.

    Returns:
        dict: {
            resume_score,
            ats_score,
            best_role,
            missing_skills,
            strengths,
            improvements,
            summary
        }
    """

    # Prompt for ATS-style structured analysis
    prompt = f"""
Act as a professional ATS (Applicant Tracking System) and resume analyzer.

Analyze the following resume and return response ONLY in valid JSON.

Resume:
{resume_text}

Return JSON in this format:

{{
  "resume_score": 0,
  "ats_score": 0,
  "best_role": "",
  "missing_skills": [],
  "strengths": [],
  "improvements": [],
  "summary": ""
}}

Rules:
- resume_score out of 100
- ats_score out of 100
- Be strict and realistic
- Return ONLY JSON, no extra text
"""

    try:
        # Call Groq LLM
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )

        result = chat_completion.choices[0].message.content.strip()

        # Remove markdown formatting if LLM adds ```json ```
        cleaned = re.sub(r"```json|```", "", result).strip()

        # Convert JSON string → Python dictionary
        data = json.loads(cleaned)

        return data

    except json.JSONDecodeError:
        print("⚠ AI returned invalid JSON format")
        return {"error": "Invalid AI JSON response"}

    except Exception as e:
        print("Groq API Error:", e)
        return {"error": "AI service failed"}