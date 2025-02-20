# # from bson import ObjectId
# # from fastapi import APIRouter, HTTPException
# # # from app.database import collection  # Import your MongoDB collection
# # from app.database import resume_collection  # ✅ Correct import

# # router = APIRouter()

# # # ✅ Helper function to convert MongoDB document
# # def serialize_document(doc):
# #     """Convert ObjectId to string in MongoDB document."""
# #     if "_id" in doc:
# #         doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
# #     return doc

# # # ✅ Example Route (Fetching Resumes)
# # @router.get("/resumes")
# # async def get_resumes():
# #     """Fetch all resumes from MongoDB and convert ObjectId."""
# #     try:
# #         resumes = collection.find()  # Fetch all documents
# #         resume_list = [serialize_document(doc) for doc in resumes]
# #         return {"resumes": resume_list}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))
# # from bson import ObjectId

# # @app.post("/api/upload")
# # async def upload_resume(file: UploadFile = File(...)):
# #     file_id = fs.put(file.file, filename=file.filename)
    
# #     resume_data = {
# #         "filename": file.filename,
# #         "file_id": str(file_id)  # Convert ObjectId to string
# #     }
    
# #     resume_collection.insert_one(resume_data)

# #     return {"message": "File uploaded successfully", "file_id": str(file_id)}

# from bson import ObjectId

# @app.post("/api/upload")
# async def upload_resume(file: UploadFile = File(...)):
#     file_id = fs.put(file.file, filename=file.filename)
    
#     resume_data = {
#         "filename": file.filename,
#         "file_id": str(file_id)  # ✅ Convert ObjectId to string
#     }
    
#     resume_collection.insert_one(resume_data)

#     return {"message": "File uploaded successfully", "file_id": str(file_id)}
# from bson import ObjectId

# @app.post("/api/upload")
# async def upload_resume(file: UploadFile = File(...)):
#     file_id = fs.put(file.file, filename=file.filename)
    
#     resume_data = {
#         "filename": file.filename,
#         "file_id": str(file_id)  # ✅ Convert ObjectId to string
#     }
    
#     inserted = resume_collection.insert_one(resume_data)
#     inserted_id = inserted.inserted_id  # ✅ MongoDB `_id` field

#     response = {
#         "message": "File uploaded successfully",
#         "file_id": str(file_id),
#         "inserted_id": str(inserted_id)  # ✅ Convert `_id` to string
#     }

#     print(response)  # ✅ Debugging output

#     return response
from fastapi.responses import JSONResponse

@app.post("/api/upload")
async def upload_resume(file: UploadFile = File(...)):
    file_id = fs.put(file.file, filename=file.filename)
    
    resume_data = {
        "filename": file.filename,
        "file_id": str(file_id)  # ✅ Convert ObjectId to string
    }
    
    inserted = resume_collection.insert_one(resume_data)
    inserted_id = inserted.inserted_id  # ✅ MongoDB `_id` field

    response = {
        "message": "File uploaded successfully",
        "file_id": str(file_id),
        "inserted_id": str(inserted_id)  # ✅ Convert `_id` to string
    }

    return JSONResponse(content=response)  # ✅ Force JSON-safe response
