# User table model for authentication system

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, index=True)
    password = Column(String(200))
    created_at = Column(TIMESTAMP, server_default=func.now())