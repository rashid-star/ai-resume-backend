# ==========================================================
# RESUME MODEL
# Stores uploaded resumes and AI analysis results
# ==========================================================

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.sql import func
from database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    # -------------------------
    # BASIC INFO
    # -------------------------

    id = Column(Integer, primary_key=True, index=True)

    # User who uploaded the resume
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Original resume filename
    filename = Column(String(255), nullable=False)

    # Extracted resume text
    content = Column(Text, nullable=True)

    # -------------------------
    # AI ANALYSIS RESULTS
    # -------------------------

    # Overall resume score
    score = Column(Float, nullable=True)

    # ATS compatibility score
    ats_score = Column(Float, nullable=True)

    # Best predicted job role
    best_role = Column(String(255), nullable=True)

    # Resume summary
    summary = Column(Text, nullable=True)

    # Candidate strengths
    strengths = Column(Text, nullable=True)

    # Missing skills
    missing_skills = Column(Text, nullable=True)

    # Suggested improvements
    improvements = Column(Text, nullable=True)

    # Raw AI response (optional debugging)
    analysis = Column(Text, nullable=True)

    # -------------------------
    # TIMESTAMP
    # -------------------------

    created_at = Column(DateTime(timezone=True), server_default=func.now())