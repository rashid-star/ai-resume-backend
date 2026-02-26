# ============================================
# JWT TOKEN HANDLER
# Responsible for creating access tokens
# ============================================

from jose import jwt
from datetime import datetime, timedelta

# Secret key for JWT encoding (change in production)
SECRET_KEY = "mysecretkey123"

# JWT algorithm
ALGORITHM = "HS256"

# Token expiry time (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    """
    Creates JWT access token for authenticated users.

    Steps:
    1. Copy user data (usually user_id)
    2. Add expiration time
    3. Encode JWT token
    4. Return token
    """

    # Copy payload data
    to_encode = data.copy()

    # Set token expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiry to payload
    to_encode.update({"exp": expire})

    # Encode JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt