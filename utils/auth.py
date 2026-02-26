# ============================================
# AUTH MIDDLEWARE - GET CURRENT LOGGED-IN USER
# ============================================

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from database.connection import SessionLocal
from models.user import User
from utils.jwt_handler import SECRET_KEY, ALGORITHM

# Security scheme for extracting Bearer token from header
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Extracts and verifies JWT token from request header.

    Steps:
    1. Get token from Authorization header
    2. Decode JWT token
    3. Fetch user from database
    4. Return current logged-in user

    Used as dependency in protected routes.
    """

    # Extract token from "Bearer <token>"
    token = credentials.credentials

    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Create DB session
    db = SessionLocal()

    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user