from fastapi import APIRouter, HTTPException
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

@router.get("/details/{resume_id}")
async def get_resume(resume_id: str):
    try:
        document = resume_collection.find_one({"_id": ObjectId(resume_id)})  # ✅ Correct collection name
        if document:
            return convert_objectid(document)  # ✅ Convert ObjectId
        raise HTTPException(status_code=404, detail="Resume not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid resume ID format: {str(e)}")
