# ================================
# IMPORTS SECTION
# ================================

from fastapi.middleware.cors import CORSMiddleware

# Admin routes
from admin_routes import router as admin_router

# AI analysis service (Groq)
from services.groq_service import analyze_resume_with_ai

# Resume PDF text extraction
import fitz  # PyMuPDF

# File handling
import os
import shutil
from fastapi import HTTPException, UploadFile, File

# Database models
from models.resume import Resume
from models.user import User

# Auth & security utilities
from utils.auth import get_current_user
from utils.security import verify_password, hash_password
from utils.jwt_handler import create_access_token

# Schemas (request/response)
from schemas.user_schema import UserLogin, UserCreate

# Database setup
from database.base import Base
from database.connection import engine, get_db

# FastAPI & DB
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


# ================================
# FASTAPI APP INITIALIZATION
# ================================

app = FastAPI(title="AI Resume Analyzer Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include admin routes (admin panel APIs)
app.include_router(admin_router)

# Create database tables automatically
Base.metadata.create_all(bind=engine)


# ================================
# BASIC TEST ROUTES
# ================================

# Root route to check backend is running
@app.get("/")
def home():
    return {"msg": "Backend running successfully 🚀"}


# Database connection test route
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    """
    This endpoint checks whether database connection is working.
    Used only for testing purposes.
    """
    return {"msg": "Database connected successfully ✅"}

# ================================
# USER AUTHENTICATION APIs
# ================================

# Register new user
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    - Checks if email already exists
    - Hashes password
    - Stores user in database
    """

    # Check if email already registered
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password before saving
    hashed_pw = hash_password(user.password)

    # Create new user object
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# User login API
@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT token.
    - Verifies email exists
    - Checks password
    - Returns access token
    """

    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        return {"error": "Invalid email"}

    # Verify password
    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid password"}

    # Generate JWT token
    token = create_access_token({"user_id": db_user.id})

    return {
        "message": "Login successful",
        "access_token": token
    }


# Get current logged-in user profile
@app.get("/me")
def get_me(current_user = Depends(get_current_user)):
    """
    Returns currently logged-in user details.
    Requires JWT token.
    """

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


# ================================
# RESUME UPLOAD & AI ANALYSIS
# ================================

# Upload resume, extract text, analyze with AI and save in DB
@app.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Upload resume endpoint:
    - Saves uploaded PDF
    - Extracts text from resume
    - Sends to AI (Groq) for analysis
    - Saves score + insights in database
    """

    # Ensure uploads folder exists
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    # Save uploaded file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF using PyMuPDF
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    # --- AI ANALYSIS ---
    ai_result = analyze_resume_with_ai(text)

    # Extract values from AI result
    resume_score = ai_result.get("resume_score")
    ats_score = ai_result.get("ats_score")
    best_role = ai_result.get("best_role")
    missing_skills = ",".join(ai_result.get("missing_skills", []))
    strengths = ",".join(ai_result.get("strengths", []))
    improvements = ",".join(ai_result.get("improvements", []))
    summary = ai_result.get("summary")

    # Save resume + analysis into database
    new_resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        content=text,   # ← THIS MUST EXIST
        score=resume_score,
        ats_score=ats_score,
        best_role=best_role,
        missing_skills=missing_skills,
        strengths=strengths,
        improvements=improvements,
        summary=summary,
        analysis=str(ai_result)
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "message": "Resume uploaded and analyzed successfully 🚀",
        "resume_id": new_resume.id,
        "user": current_user.email,
        "resume_score": resume_score,
        "best_role": best_role
    }

# ================================
# USER RESUME HISTORY APIs
# ================================

# Get all resumes uploaded by current user
@app.get("/my-resumes")
def get_my_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns all resumes uploaded by logged-in user.
    Used for dashboard/history page.
    """

    user_id = current_user.id

    resumes = db.query(Resume).filter(
        Resume.user_id == user_id
    ).order_by(Resume.created_at.desc()).all()

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
            "domain": r.domain,
            "created_at": r.created_at
        })

    return {"resumes": data}


# Get best resume based on score
@app.get("/best-resume")
def get_best_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns highest scoring resume of user.
    Useful for resume comparison feature.
    """

    best = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(Resume.resume_score.desc()).first()

    if not best:
        return {"message": "No resumes found"}

    return {
        "filename": best.filename,
        "resume_score": best.resume_score,
        "ats_score": best.ats_score,
        "best_role": best.best_role
    }


# ================================
# USER DASHBOARD API
# ================================

# Dashboard statistics for logged-in user
@app.get("/my-dashboard")
def my_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    User dashboard summary:
    - total resumes
    - average score
    - best resume
    - full resume details
    """

    user_id = current_user.id
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
        .all()
    )
    # If no resumes, return safe empty structure
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
        "best_resume_score": best_resume.score or 0,
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
                "domain": r.domain,
                "created_at": r.created_at
            }
            for r in resumes
        ]
    }

# ================================
# ADMIN PANEL APIs
# ================================

from admin_utils import admin_required
from sqlalchemy import func


# Get all users (admin only)
@app.get("/admin/all-users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):
    """
    Admin endpoint:
    Returns all registered users.
    """
    users = db.query(User).all()
    return users


# Get all resumes in system (admin only)
@app.get("/admin/all-resumes")
def get_all_resumes(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):
    """
    Admin endpoint:
    View all resumes uploaded by all users.
    """
    resumes = db.query(Resume).all()
    return resumes


# Admin dashboard stats
@app.get("/admin/stats")
def admin_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):
    """
    Admin statistics:
    - total users
    - total resumes
    - average resume score
    """

    total_users = db.query(User).count()
    total_resumes = db.query(Resume).count()
    avg_score = db.query(func.avg(Resume.score)).scalar()

    return {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "average_resume_score": avg_score
    }