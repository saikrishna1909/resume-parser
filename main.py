import os
import pdfplumber
import json
from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import google.generativeai as genai
from langchain_community.chat_models import ChatGoogle
from langchain.schema import HumanMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("⚠️ Missing GEMINI_API_KEY in .env file!")

genai.configure(api_key=GEMINI_API_KEY)
chat_model = ChatGoogle(model="gemini-pro")

# FastAPI app
app = FastAPI()

# SQLite Database
DATABASE_URL = "sqlite:///./resumes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Resume Database Model
class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    core_skills = Column(Text, nullable=True)  # JSON stored as string
    soft_skills = Column(Text, nullable=True)
    resume_rating = Column(Integer, nullable=True)
    improvement_areas = Column(Text, nullable=True)
    upskill_suggestions = Column(Text, nullable=True)
    file_name = Column(String, nullable=False)

# Create the database if it doesn't exist
Base.metadata.create_all(bind=engine)

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text

# Analyze Resume using Gemini AI
def analyze_resume(text):
    prompt = f"""
    Extract and structure the following details from this resume:
    - Name
    - Email
    - Phone Number
    - Core Technical Skills
    - Soft Skills
    - Work Experience Summary
    - Resume Rating (out of 10)
    - Areas for Improvement
    - Suggested Skills to Learn

    Resume Text:
    {text}
    """

    response = chat_model.invoke([HumanMessage(content=prompt)])
    try:
        return json.loads(response.content)
    except:
        return {}

# API to Upload and Process Resume
@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    text = extract_text_from_pdf(file_path)
    resume_data = analyze_resume(text)

    resume_entry = Resume(
        name=resume_data.get("name", "Unknown"),
        email=resume_data.get("email", "Unknown"),
        phone=resume_data.get("phone", ""),
        core_skills=json.dumps(resume_data.get("core_skills", [])),
        soft_skills=json.dumps(resume_data.get("soft_skills", [])),
        resume_rating=resume_data.get("resume_rating", 0),
        improvement_areas=resume_data.get("improvement_areas", ""),
        upskill_suggestions=resume_data.get("upskill_suggestions", ""),
        file_name=file.filename
    )

    db.add(resume_entry)
    db.commit()
    db.refresh(resume_entry)

    return resume_data

# API to Retrieve All Uploaded Resumes
@app.get("/resumes/")
def get_all_resumes(db: Session = Depends(get_db)):
    return db.query(Resume).all()

# API to Get Resume Details
@app.get("/resume/{resume_id}")
def get_resume_details(resume_id: int, db: Session = Depends(get_db)):
    return db.query(Resume).filter(Resume.id == resume_id).first()
