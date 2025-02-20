from fastapi import APIRouter
from app.database import resume_collection  # ✅ Correct collection name
from bson import ObjectId

def convert_objectid(document):
    """Convert MongoDB ObjectId to a string recursively in a document"""
    if isinstance(document, list):
        return [convert_objectid(item) for item in document]
    elif isinstance(document, dict):
        return {key: str(value) if isinstance(value, ObjectId) else value for key, value in document.items()}
    return document

router = APIRouter()

@router.get("/history")
async def get_all_resumes():
    resumes = list(resume_collection.find())  # ✅ Fixed: Use resume_collection
    return convert_objectid(resumes)  # ✅ Convert ObjectId before returning
