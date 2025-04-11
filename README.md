# resume-parser


📄 Resume Parser
A web-based Resume Parser that extracts key details from resumes (PDF/DOCX), stores them in MongoDB (GridFS), and provides skill enhancement suggestions using Gemini API with Langchain.

### 🚀 Features
✅ Upload and extract key resume details (skills, experience, education, contact info).
✅ Store resumes in MongoDB GridFS and extracted data in MongoDB Collections.
✅ Display historical resumes with extracted details in a tabular format.
✅ Gemini API integration for skill improvement suggestions.
✅ Minimal and neat React frontend for easy navigation.

### 🏗️ Project Structure
bash
Copy
Edit
resume-parser/
│── backend/              # Backend (FastAPI)
│   ├── app/             
│   │   ├── routes/       # API Routes
│   │   ├── models.py     # MongoDB Models
│   │   ├── database.py   # MongoDB Connection
│   │   ├── resume_extraction.py  # Resume Parsing Logic
│   │   ├── main.py       # FastAPI Main Entry
│   │   ├── test_mongo.py # MongoDB Connection Test
│   ├── requirements.txt  # Backend Dependencies
│
│── frontend/             # Frontend (React)
│   ├── src/              # React Source Code
│   ├── package.json      # Frontend Dependencies
│
│── .gitignore
│── README.md
│── main.py


### 🛠️ Tech Stack

## 🌐 Frontend
React.js (Vite)
Axios (API Calls)
CSS (Normal CSS for styling)

## ⚙️ Backend

FastAPI (Python Web Framework)
MongoDB Atlas + GridFS (Resume Storage)
Langchain + Gemini API (Skill Suggestion)
Pydantic (Data Validation)

### ⚙️ Setup Instructions
🔹 1. Clone the Repository
sh
Copy
Edit
git clone https://github.com/your-username/resume-parser.git
cd resume-parser
🔹 2. Setup MongoDB
Create a MongoDB Atlas account.
Get the MongoDB Connection String and update backend/app/database.py:
python
Copy
Edit
MONGO_URI = "your-mongodb-connection-string"
🔹 3. Run Backend (FastAPI)
sh
Copy
Edit
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Backend Running on: http://127.0.0.1:8000

🔹 4. Run Frontend (React)
sh
Copy
Edit
cd frontend
npm install
npm run dev
Frontend Running on: http://localhost:5173

### 📂 API Endpoints
📌 Upload Resume
POST /upload
Request: Upload a PDF/DOCX file
Response: Extracted Resume Details

📌 Get Resume History
GET /history
Response: List of all past resumes

📌 Download Resume
GET /download/{resume_id}
Response: Resume file from GridFS

** FIND THE DEPLOYMENTS UNDER THE DEPLOYMENT LINKS ON THE RIGHT SIDE OF THE CODE
