🚀 AI Resume Analyzer – Frontend

A modern web interface for the AI Resume Analyzer platform that allows users to upload resumes and receive AI-powered insights including resume score, ATS compatibility, strengths, missing skills, and improvement suggestions.

This frontend is built using React and TailwindCSS and communicates with the FastAPI backend to perform AI analysis.

🌐 Live Demo

👉 https://ai-resume-frontend-sigma.vercel.app

✨ Features

🔐 User Authentication (Register & Login)

📄 Resume Upload (PDF)

🤖 AI-Powered Resume Analysis

📊 Resume Score & ATS Score

💡 Strengths Detection

⚠️ Missing Skills Identification

🛠 Resume Improvement Suggestions

📂 Dashboard to view previous resume analyses

🌙 Dark Mode UI

🛠 Tech Stack

Frontend Framework

React

Styling

Tailwind CSS

Icons

Lucide

HTTP Requests

Axios

Deployment

Vercel

Backend API

FastAPI

AI Integration

Groq

📂 Project Structure
src
│
├── components
│   ├── Navbar.jsx
│   ├── ResumeCard.jsx
│   └── StatsCard.jsx
│
├── pages
│   ├── Dashboard.jsx
│   ├── Upload.jsx
│   ├── Login.jsx
│   └── Register.jsx
│
├── api
│   └── api.js
│
├── App.jsx
└── main.jsx
⚙️ Setup Instructions

Clone the repository

git clone https://github.com/your-username/ai-resume-frontend.git
cd ai-resume-frontend

Install dependencies

npm install

Run the development server

npm run dev

Open in browser

http://localhost:5173
🔗 Backend API

This frontend communicates with the backend API deployed on Railway.

Example API Base URL:

https://ai-resume-backend-production-f355.up.railway.app
🧠 How It Works

User registers and logs in.

User uploads a resume in PDF format.

The resume is sent to the backend API.

The backend extracts resume text and sends it to an AI model.

AI analyzes the resume and returns structured insights.

Results are displayed in the dashboard.

📸 UI Highlights

Animated resume cards

Expandable analysis sections

Score visualization

Skill tags for strengths and missing skills

Responsive design

🚀 Deployment

The frontend is deployed on:

Vercel

Deployment is automatic when pushing changes to GitHub.

👨‍💻 Author

Mohammad Rashid
Aspiring AI / Machine Learning Engineer
