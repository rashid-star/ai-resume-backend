from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.connection import get_db
from models.user import User
from models.resume import Resume
from admin_utils import admin_required

router = APIRouter(prefix="/admin", tags=["Admin"])


# 🔹 all users
@router.get("/all-users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):
    users = db.query(User).all()
    return users


# 🔹 all resumes
@router.get("/all-resumes")
def get_all_resumes(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):
    resumes = db.query(Resume).all()
    return resumes


# 🔹 stats
@router.get("/stats")
def admin_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):
    total_users = db.query(User).count()
    total_resumes = db.query(Resume).count()
    avg_score = db.query(func.avg(Resume.score)).scalar()

    return {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "average_resume_score": avg_score
    }