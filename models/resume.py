# SQLAlchemy model for storing user resumes and AI analysis

from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, Float, DateTime
from sqlalchemy.sql import func
from database.base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255))
    content = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # AI fields
    analysis = Column(Text, nullable=True)
    ats_score = Column(Float, nullable=True)
    best_role = Column(String(255), nullable=True)
    strengths = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    domain = Column(String(100), nullable=True)
    skills = Column(Text, nullable=True)
    missing_skills = Column(Text, nullable=True)
    predicted_role = Column(Text, nullable=True)
    improvements = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())