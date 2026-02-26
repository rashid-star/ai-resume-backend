from fastapi import HTTPException, Depends
from models.user import User
from utils.auth import get_current_user   # adjust if your file name different

ADMIN_EMAIL = "chaudharyrasid31@gmail.com"   # put your login email

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.email != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user