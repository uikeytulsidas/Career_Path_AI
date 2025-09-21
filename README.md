# Career Path Analyzer #
AI-powered career guidance platform that extracts skills from resumes, recommends career paths, and provides a personalized learning roadmap.

📌 Problem Statement

Job seekers and students often:
Struggle to identify suitable career paths.
Lack clarity on the skills required for their desired role.
Have resumes that don’t clearly reflect skill gaps.


💡 Our Solution:-
Career Path Analyzer bridges this gap using AI :
📄 Resume parsing & skill extraction.
🧭 Career path recommendations.
📚 Personalized learning roadmap with curated resources.
💬 Chat-like interactive guidance with saved sessions.

✨Key Features:-
AI-powered skill extraction from resumes.
Tailored career path recommendations.
Personalized learning roadmap.
Interactive chat interface with history.
JWT-based authentication (optional).

🛠️ Tech Stack:-
Frontend: React.js
Backend: Django + PostgreSQL
AI/ML: Google Gemini API (via Google Cloud)
Hosting: Render (backend), Firebase/Vercel (frontend)



📸 Demo Screenshots

<img width="1892" height="881" alt="Screenshot 2025-09-16 234915" src="https://github.com/user-attachments/assets/6a3e7150-92f6-4bf7-b64a-f0625765935f" />

<img width="1881" height="880" alt="Screenshot 2025-09-16 234957" src="https://github.com/user-attachments/assets/dca7ddde-b173-478d-b463-d9b6ed174bd1" />
AI-generated career recommendations
Chat sidebar with saved sessions
Authentication flow




1. Clone Repo
git clone https://github.com/uikeytulsidas/AI_backend.git
cd backend

2. Backend Setup (Django)
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

3. Frontend Setup (React)
cd frontend
npm install
npm start


4. Environment Variables
Create .env in both backend/ and frontend/:-
Backend (backend/.env):

GEMINI_API_KEY=your_google_gemini_api_key
DATABASE_URL=postgres://user:password@localhost:5432/careerdb
SECRET_KEY=your_django_secret_key

Frontend (frontend/.env):-

REACT_APP_API_URL=http://localhost:8000/api


