from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.database import fs  # ✅ GridFS instance
from bson import ObjectId
import io

router = APIRouter()


@router.get("/download/{file_id}")
async def download_resume(file_id: str):
    try:
        file = fs.get(ObjectId(file_id))  # ✅ Convert file_id to ObjectId
        return StreamingResponse(
            io.BytesIO(file.read()), 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={file.filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found or invalid ID: {str(e)}")
