# # from fastapi import APIRouter, File, UploadFile, HTTPException
# # from app.database import fs, resume_collection
# # from app.resume_extraction import extract_text_from_pdf, extract_resume_info
# # from bson import ObjectId

# # # ✅ Define Router Instance
# # router = APIRouter()

# # @router.post("/upload")
# # async def upload_resume(file: UploadFile = File(...)):
# #     try:
# #         # ✅ Validate File Type
# #         allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
# #         if file.content_type not in allowed_types:
# #             raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are supported.")

# #         # ✅ Read File Contents
# #         file_contents = await file.read()

# #         # ✅ Save File to MongoDB GridFS
# #         file_id = fs.put(file_contents, filename=file.filename)

# #         # ✅ Extract text from PDF
# #         extracted_text = extract_text_from_pdf(file_contents)

# #         if not extracted_text.strip():
# #             raise HTTPException(status_code=400, detail="Failed to extract text from the resume.")

# #         # ✅ Use Gemini API to extract structured data
# #         extracted_data = extract_resume_info(extracted_text)

# #         if "error" in extracted_data:
# #             raise HTTPException(status_code=500, detail=extracted_data["error"])

# #         # ✅ Store structured data in MongoDB
# #         resume_data = {
# #             "file_id": str(file_id),  # ✅ Convert ObjectId to String
# #             "filename": file.filename,
# #             **extracted_data  # ✅ Merge extracted data into dictionary
# #         }
# #         inserted_resume = resume_collection.insert_one(resume_data)

# #         # ✅ Return Clean Response
# #         return {
# #             "message": "Resume uploaded successfully",
# #             "resume_id": str(inserted_resume.inserted_id),  # ✅ Convert ObjectId to string
# #             "resume_data": resume_data
# #         }

# #     except HTTPException as http_ex:
# #         raise http_ex  # ✅ Properly raise HTTPException
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# # # ✅ Ensure the router is properly exported
# # __all__ = ["router"]
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from pymongo import MongoClient
# from gridfs import GridFS
# from bson import ObjectId

# app = FastAPI()

# # MongoDB Connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client["resume_db"]
# fs = GridFS(db)
# resume_collection = db["resumes"]

# @app.post("/api/upload")
# async def upload_resume(file: UploadFile = File(...)):
#     file_id = fs.put(file.file, filename=file.filename)
    
#     # Insert resume metadata into MongoDB
#     resume_data = {
#         "filename": file.filename,
#         "file_id": str(file_id)  # ✅ Convert ObjectId to string
#     }
    
#     inserted = resume_collection.insert_one(resume_data)
    
#     response = {
#         "message": "File uploaded successfully",
#         "file_id": str(file_id),  # ✅ Convert ObjectId to string
#         "inserted_id": str(inserted.inserted_id)  # ✅ Convert `_id` to string
#     }

#     return JSONResponse(content=response)  # ✅ Ensures proper JSON serialization
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
import traceback

app = FastAPI()

# MongoDB Connection
try:
    client = MongoClient("mongodb+srv://kondasaikrishna13:W26yfBzEOZPjMkdC@cluster0.ij6bm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["resume_db"]
    fs = GridFS(db)
    resume_collection = db["resumes"]
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed:", str(e))

@app.post("/api/upload")
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
