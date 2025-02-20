from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
import traceback

router = APIRouter()  # ✅ Define router instance

# MongoDB Connection
try:
    client = MongoClient("mongodb+srv://kondasaikrishna13:W26yfBzEOZPjMkdC@cluster0.ij6bm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["resume_db"]
    fs = GridFS(db)
    resume_collection = db["resumes"]
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed:", str(e))

@router.post("/upload")  # ✅ Use router instead of app
async def upload_resume(file: UploadFile = File(...)):
    try:
        print(f"📂 Uploading file: {file.filename}")

        # Store file in GridFS
        file_id = fs.put(file.file, filename=file.filename)
        print(f"✅ File stored in GridFS with ID: {file_id}")

        # Insert resume metadata into MongoDB
        resume_data = {
            "filename": file.filename,
            "file_id": str(file_id)  # ✅ Convert ObjectId to string
        }
        inserted = resume_collection.insert_one(resume_data)
        print(f"✅ Metadata inserted into MongoDB with ID: {inserted.inserted_id}")

        response = {
            "message": "File uploaded successfully",
            "file_id": str(file_id),  # ✅ Convert ObjectId to string
            "inserted_id": str(inserted.inserted_id)  # ✅ Convert `_id` to string
        }

        return JSONResponse(content=response)

    except Exception as e:
        print("❌ Error during file upload:", str(e))
        print(traceback.format_exc())  # Print full error traceback
        raise HTTPException(status_code=500, detail="Internal Server Error")
