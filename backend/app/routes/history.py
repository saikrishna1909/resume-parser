from fastapi import APIRouter, HTTPException
from app.database import resume_collection  # ✅ Correct collection name
from bson import ObjectId

router = APIRouter()

def convert_objectid(document):
    """Convert MongoDB ObjectId to a string recursively in a document."""
    if isinstance(document, list):
        return [convert_objectid(item) for item in document]
    elif isinstance(document, dict):
        return {key: str(value) if isinstance(value, ObjectId) else value for key, value in document.items()}
    return document

@router.get("/history")
async def get_all_resumes():
    try:
        resumes = list(resume_collection.find({}, {"_id": 1, "filename": 1, "file_id": 1}))  # ✅ Fetch specific fields only
        
        if not resumes:
            return {"resumes": []}  # ✅ Return an empty list if no resumes are found

        return {"resumes": convert_objectid(resumes)}  # ✅ Wrap response in a dictionary
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
