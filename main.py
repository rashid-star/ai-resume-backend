# ==========================================================
# AI RESUME ANALYZER - MAIN BACKEND FILE
# FastAPI application entry point
# ==========================================================

# -------------------------
# IMPORTS
# -------------------------

# FastAPI core
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Database
from sqlalchemy.orm import Session
from database.base import Base
from database.connection import engine, get_db

# Models
from models.user import User
from models.resume import Resume

# Schemas
from schemas.user_schema import UserLogin, UserCreate

# Auth utilities
from utils.security import verify_password, hash_password
from utils.jwt_handler import create_access_token
from utils.auth import get_current_user

# AI analysis service
from services.groq_service import analyze_resume_with_ai

# Resume text extraction
import fitz  # PyMuPDF

# File handling
import os
import shutil


# ==========================================================
# FASTAPI INITIALIZATION
# ==========================================================

app = FastAPI(title="AI Resume Analyzer Backend")

# Enable CORS so frontend can communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production use frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Automatically create database tables
Base.metadata.create_all(bind=engine)


# ==========================================================
# BASIC ROUTES
# ==========================================================

@app.get("/")
def home():
    """
    Simple health check route
    """
    return {"message": "AI Resume Analyzer Backend Running 🚀"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    """
    Check if database connection is working
    """
    return {"message": "Database connected successfully ✅"}


# ==========================================================
# USER AUTHENTICATION
# ==========================================================

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register new user
    """

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = hash_password(user.password)

    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT token
    """

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"user_id": db_user.id})

    return {
        "message": "Login successful",
        "access_token": token
    }


@app.get("/me")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get logged-in user profile
    """

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


# ==========================================================
# RESUME UPLOAD & AI ANALYSIS
# ==========================================================

@app.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload resume and analyze using AI
    """

    # Ensure uploads folder exists
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -------------------------
    # Extract text from PDF
    # -------------------------

    try:
        doc = fitz.open(file_path)
        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to read PDF")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Resume text extraction failed")

    # -------------------------
    # AI ANALYSIS
    # -------------------------

    ai_result = analyze_resume_with_ai(text)

    # Ensure safe values (avoid None in DB)
    resume_score = ai_result.get("resume_score", 0)
    ats_score = ai_result.get("ats_score", 0)
    best_role = ai_result.get("best_role", "N/A")
    summary = ai_result.get("summary", "No summary available")

    strengths = ai_result.get("strengths", [])
    missing_skills = ai_result.get("missing_skills", [])
    improvements = ai_result.get("improvements", [])

    # Convert lists → string for DB storage
    strengths = ", ".join(strengths) if isinstance(strengths, list) else strengths
    missing_skills = ", ".join(missing_skills) if isinstance(missing_skills, list) else missing_skills
    improvements = ", ".join(improvements) if isinstance(improvements, list) else improvements

    # -------------------------
    # Save to database
    # -------------------------

    new_resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        content=text,
        score=resume_score,
        ats_score=ats_score,
        best_role=best_role,
        strengths=strengths,
        missing_skills=missing_skills,
        improvements=improvements,
        summary=summary,
        analysis=str(ai_result)
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "message": "Resume uploaded and analyzed successfully",
        "resume_id": new_resume.id,
        "resume_score": resume_score,
        "best_role": best_role
    }


# ==========================================================
# USER RESUME HISTORY
# ==========================================================

@app.get("/my-resumes")
def get_my_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Return all resumes uploaded by the user
    """

    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )

    data = []

    for r in resumes:
        data.append({
            "id": r.id,
            "filename": r.filename,
            "resume_score": r.score,
            "ats_score": r.ats_score,
            "best_role": r.best_role,
            "summary": r.summary,
            "strengths": r.strengths,
            "missing_skills": r.missing_skills,
            "improvements": r.improvements,
            "created_at": r.created_at
        })

    return {"resumes": data}


# ==========================================================
# USER DASHBOARD
# ==========================================================

@app.get("/my-dashboard")
def my_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Dashboard statistics for user
    """

    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )

    if not resumes:
        return {
            "total_resumes": 0,
            "average_score": 0,
            "best_resume_score": 0,
            "resumes": []
        }

    total = len(resumes)

    avg_score = sum([r.score or 0 for r in resumes]) / total

    best_resume = max(resumes, key=lambda x: x.score or 0)

    return {
        "total_resumes": total,
        "average_score": round(avg_score, 2),
        "best_resume_score": best_resume.score,
        "resumes": [
            {
                "id": r.id,
                "filename": r.filename,
                "resume_score": r.score,
                "ats_score": r.ats_score,
                "best_role": r.best_role,
                "summary": r.summary,
                "strengths": r.strengths,
                "missing_skills": r.missing_skills,
                "improvements": r.improvements,
                "created_at": r.created_at
            }
            for r in resumes
        ]
    }