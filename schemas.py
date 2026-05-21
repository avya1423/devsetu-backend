from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from models import RoleEnum, DifficultyEnum

# ----- User Schemas -----
class UserBase(BaseModel):
    github_handle: str
    full_name: str
    role: Optional[RoleEnum] = RoleEnum.student
    graduation_year: Optional[int] = None
    academic_path: Optional[str] = None
    primary_skills: Optional[List[str]] = []

class UserCreate(UserBase):
    pass 

class UserResponse(UserBase):
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True 

# ----- Project Schemas -----
class ProjectBase(BaseModel):
    title: str
    description: str
    difficulty: DifficultyEnum
    required_stack: List[str]
    github_template_url: Optional[str] = None
    estimated_hours: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    project_id: UUID

    class Config:
        from_attributes = True