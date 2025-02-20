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
        if not ObjectId.is_valid(resume_id):  # ✅ Validate ID before converting
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        document = resume_collection.find_one({"_id": ObjectId(resume_id)})  # ✅ Correct collection name
        
        if not document:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return convert_objectid(document)  # ✅ Convert ObjectId to string
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
