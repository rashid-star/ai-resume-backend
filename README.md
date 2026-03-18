🚀 AI Resume Analyzer – Backend

This is the backend API for the AI Resume Analyzer project.

Built using FastAPI, this service handles authentication, resume uploads, AI analysis, and database storage. It communicates with the frontend and processes resumes using an AI model.

The backend is responsible for:

User authentication

Resume text extraction

AI-powered resume analysis

Storing results in a database

Providing dashboard data through APIs

📌 Features

🔐 User Authentication (Register / Login)

📄 Resume Upload (PDF)

🧠 AI Resume Analysis

📊 Resume Score & ATS Score

💡 Strengths Detection

⚠️ Missing Skills Identification

🛠 Resume Improvement Suggestions

📂 Resume History Dashboard API

🔑 JWT Token Authentication

🛠 Tech Stack
Technology	Usage
FastAPI	Backend framework
SQLAlchemy	ORM for database
MySQL	Database
PyMuPDF	PDF text extraction
Groq API	AI resume analysis
JWT	Authentication
Uvicorn	ASGI server
🖥 How To Run This Project
1️⃣ Clone Repository
git clone https://github.com/rashid-star/ai-resume-backend.git
cd ai-resume-backend
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Setup Environment Variables

Create a .env file in the project root:

DATABASE_URL=your_database_connection_url
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_jwt_secret_key
4️⃣ Run Backend Server
uvicorn main:app --reload

Server will run at:

http://127.0.0.1:8000

API documentation available at:

http://127.0.0.1:8000/docs
🔗 Frontend Requirement

This backend is used by the frontend application.

Frontend Repository:

👉 https://github.com/rashid-star/ai-resume-frontend

Frontend runs at:

http://localhost:5173
📁 Project Structure
ai-resume-backend/
│
├── database/
│   ├── base.py
│   └── connection.py
│
├── models/
│   ├── user.py
│   └── resume.py
│
├── schemas/
│   └── user_schema.py
│
├── services/
│   └── groq_service.py
│
├── utils/
│   ├── auth.py
│   ├── jwt_handler.py
│   └── security.py
│
├── uploads/
│
├── main.py
└── requirements.txt
⚙ API Endpoints
Method	Endpoint	Description
POST	/register	Register new user
POST	/login	User login
GET	/me	Get current user
POST	/upload-resume	Upload resume and analyze
GET	/my-dashboard	Get user dashboard data
🎯 Future Improvements

Job description matching

Resume keyword optimization

Resume comparison

Admin dashboard

AI interview preparation suggestions

👨‍💻 Author

Mohammad Rashid

GitHub:
https://github.com/rashid-star
