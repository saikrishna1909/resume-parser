from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router
from app.routes.history import router as history_router
from app.routes.details import router as details_router
from app.routes.download import router as download_router
from app.routes.resume_routes import router as resume_router

app = FastAPI()

# ✅ Correctly Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allows all origins, change to ["http://localhost:3000"] if needed
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # ✅ Allows all headers
)

# ✅ Register Routes
app.include_router(upload_router, prefix="/api")
app.include_router(resume_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(details_router, prefix="/api")
app.include_router(download_router, prefix="/api")

# ✅ Health Check
@app.get("/")
def home():
    return {"message": "Resume Parser API is running!"}
