from pydantic import BaseModel
from typing import List, Optional

class ResumeUpload(BaseModel):
    name: str
    email: str
    phone: str
    core_skills: List[str]
    soft_skills: List[str]
    experience: str
    education: str
    resume_rating: int
    improvement_areas: str
    upskill_suggestions: str
    file_id: str  # GridFS file ID reference
