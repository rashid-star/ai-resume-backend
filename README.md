🤖 AI Resume Analyzer (Frontend)

A modern web interface for an AI-powered Resume Analyzer that evaluates resumes and provides insights such as resume score, ATS compatibility, strengths, missing skills, and improvement suggestions.

This project demonstrates a full-stack AI application with a React frontend communicating with a FastAPI backend for AI-based resume analysis.

🚀 Live Demo

Frontend (Vercel):
https://ai-resume-frontend-sigma.vercel.app

Backend API:
https://ai-resume-backend-production-f355.up.railway.app

📌 Project Overview

The AI Resume Analyzer allows users to upload their resume in PDF format and receive automated feedback powered by an LLM.

The platform analyzes resumes and provides:

Resume Score

ATS Compatibility Score

Predicted Career Role

Strengths Detection

Missing Skills Identification

Resume Improvement Suggestions

Resume History Dashboard

🧠 Tech Stack

React

Vite

Tailwind CSS

Axios

Lucide Icons

FastAPI (Backend API)

Groq LLM (AI Analysis)

MySQL (Database)

Vercel (Frontend Deployment)

Railway (Backend Deployment)

⚙️ Application Workflow

User registers and logs into the platform.

User uploads a resume (PDF).

Resume is sent to the FastAPI backend.

Backend extracts resume text.

Text is analyzed using a Groq LLM.

AI generates structured insights.

Results are stored in MySQL.

Dashboard displays resume analysis history.

📂 Project Structure
ai-resume-frontend/
│
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── ResumeCard.jsx
│   │   └── StatsCard.jsx
│   │
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Upload.jsx
│   │   ├── Login.jsx
│   │   └── Register.jsx
│   │
│   ├── api/
│   │   └── api.js
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── package.json
└── README.md
💻 How to Run Locally
1️⃣ Clone repository
git clone https://github.com/yourusername/ai-resume-frontend.git
cd ai-resume-frontend
2️⃣ Install dependencies
npm install
3️⃣ Run development server
npm run dev

Open browser:

http://localhost:5173
🌍 Deployment

Frontend is deployed on Vercel.

Deployment is automatically triggered when pushing updates to GitHub.

🎯 Project Purpose

This project was built to demonstrate:

Full-stack AI application development

React + FastAPI integration

LLM-powered resume analysis

Cloud deployment workflow

Real-world portfolio project for AI / ML roles

👨‍💻 Author

Mohammad Rashid
Machine Learning & AI Enthusiast

⭐ If you like this project

Give it a star on GitHub ⭐
