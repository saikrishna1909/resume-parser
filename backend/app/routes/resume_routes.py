from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from bson.errors import InvalidId
import traceback
from io import BytesIO

router = APIRouter()

# ✅ MongoDB Connection
try:
    client = MongoClient("mongodb+srv://kondasaikrishna13:W26yfBzEOZPjMkdC@cluster0.ij6bm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["resume_db"]
    fs = GridFS(db)  # GridFS instance for file storage
    resume_collection = db["resumes"]
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed:", str(e))


# ✅ Upload Resume (Prevents Duplicate Filenames)
@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        print(f"📂 Uploading file: {file.filename}")

        # ✅ Prevent duplicate filenames
        if resume_collection.find_one({"filename": file.filename}):
            raise HTTPException(status_code=400, detail="File with the same name already exists")

        # ✅ Store file in GridFS
        file_id = fs.put(file.file, filename=file.filename)
        print(f"✅ File stored in GridFS with ID: {file_id}")

        # ✅ Store metadata in MongoDB
        resume_data = {"filename": file.filename, "file_id": str(file_id)}
        inserted = resume_collection.insert_one(resume_data)
        print(f"✅ Metadata inserted into MongoDB with ID: {inserted.inserted_id}")

        return JSONResponse(content={"message": "File uploaded successfully", "file_id": str(file_id), "inserted_id": str(inserted.inserted_id)})

    except Exception as e:
        print("❌ Error during file upload:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ✅ Fetch All Resumes
@router.get("/resumes")
async def get_resumes():
    try:
        resumes = list(resume_collection.find({}, {"_id": 1, "filename": 1, "file_id": 1}))
        return {"resumes": [{"_id": str(res["_id"]), "filename": res["filename"], "file_id": res["file_id"]} for res in resumes]}

    except Exception as e:
        print("❌ Error fetching resumes:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ✅ View Resume Details
@router.get("/resume/{resume_id}")
async def get_resume(resume_id: str):
    try:
        if not ObjectId.is_valid(resume_id):
            raise HTTPException(status_code=400, detail="Invalid resume ID format")

        resume = resume_collection.find_one({"_id": ObjectId(resume_id)})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        return {"_id": str(resume["_id"]), "filename": resume["filename"], "file_id": resume["file_id"]}

    except Exception as e:
        print("❌ Error fetching resume details:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ✅ Download Resume
@router.get("/download/{file_id}")
async def download_resume(file_id: str):
    try:
        if not ObjectId.is_valid(file_id):
            raise HTTPException(status_code=400, detail="Invalid file ID format")

        file_obj = fs.get(ObjectId(file_id))
        if not file_obj:
            raise HTTPException(status_code=404, detail="File not found")

        return StreamingResponse(
            BytesIO(file_obj.read()),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={file_obj.filename}"}
        )

    except Exception as e:
        print("❌ Error downloading file:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ✅ Delete Resume
# ✅ Delete Resume (Removes File from GridFS & MongoDB)
@router.delete("/resumes/{resume_id}")
async def delete_resume(resume_id: str):
    try:
        # Validate and convert resume_id to ObjectId
        if not ObjectId.is_valid(resume_id):
            raise HTTPException(status_code=400, detail="Invalid resume ID format")

        # Check if the document exists before deleting
        resume = resume_collection.find_one({"_id": ObjectId(resume_id)})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        # Delete the document
        resume_collection.delete_one({"_id": ObjectId(resume_id)})
        return {"message": "Resume deleted successfully"}

    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid resume ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")