from pymongo import MongoClient
import gridfs
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "resume_parser"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
fs = gridfs.GridFS(db)  # GridFS for storing PDF/DOCX files

# Collections
resume_collection = db["resumes"]  # Stores extracted data
