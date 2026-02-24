from database.base import Base
from database.connection import engine, get_db
from models.user import User
from schemas.user_schema import UserCreate
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"msg": "Backend running"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"msg": "DB connected"}


# 👇 ADD REGISTER API HERE (below test-db)

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    # check email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return {"error": "Email already registered"}

    # create user
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }