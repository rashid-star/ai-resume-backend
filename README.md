AI Resume Analyzer – Backend : https://ai-resume-backend-production-f355.up.railway.app/docs

Backend service for the AI Resume Analyzer, a full-stack application that analyzes resumes using AI and provides insights such as ATS score, strengths, missing skills, and improvement suggestions.

This backend is built with FastAPI and integrates with an LLM (Groq) to generate intelligent resume feedback.

Features

User authentication (Register & Login)

Resume PDF upload

Resume text extraction

AI-powered resume analysis

ATS compatibility scoring

Strength detection

Missing skills identification

Resume improvement suggestions

Dashboard API for resume history

Tech Stack

Backend Framework

FastAPI

AI Integration

Groq LLM API

Database

MySQL (hosted on Railway)

ORM

SQLAlchemy

Authentication

JWT (JSON Web Tokens)

File Processing

PyMuPDF for PDF text extraction

Deployment

Hosted on Railway

Project Structure
ai-resume-backend
│
├── database
│   ├── base.py
│   └── connection.py
│
├── models
│   ├── user.py
│   └── resume.py
│
├── schemas
│   └── user_schema.py
│
├── services
│   └── groq_service.py
│
├── utils
│   ├── auth.py
│   ├── jwt_handler.py
│   └── security.py
│
├── uploads
│
├── main.py
└── requirements.txt
API Endpoints
Authentication

Register User

POST /register

Login

POST /login

Get Current User

GET /me
Resume Analysis

Upload Resume

POST /upload-resume

Uploads a PDF resume and returns AI analysis including:

Resume Score

ATS Score

Best Career Role

Strengths

Missing Skills

Improvements

Summary

Dashboard

User Dashboard

GET /my-dashboard

Returns:

Total resumes

Average score

Best resume score

Full resume analysis history

Environment Variables

Create a .env file in the root directory.

Example:

DATABASE_URL=your_mysql_connection_url
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_secret_key
Running Locally

Clone the repository

git clone https://github.com/your-username/ai-resume-backend.git
cd ai-resume-backend

Install dependencies

pip install -r requirements.txt

Run the server

uvicorn main:app --reload

API documentation will be available at:

http://127.0.0.1:8000/docs
Live Deployment

Backend is deployed on:

Railway

Example base URL:

https://your-backend-url.railway.app
Frontend

Frontend application built with React + TailwindCSS.

Live demo:

https://ai-resume-frontend-sigma.vercel.app

Frontend hosted on Vercel.

How AI Analysis Works

User uploads a resume PDF

Backend extracts text using PyMuPDF

Resume text is sent to the Groq LLM

LLM analyzes resume and returns structured JSON

Backend stores results in MySQL

Dashboard displays analysis to the user

Future Improvements

Job description matching

Resume keyword optimization

Resume improvement suggestions with examples

Better ATS keyword analysis

Multi-resume comparison

Author

Mohammad Rashid

Machine Learning Eng
