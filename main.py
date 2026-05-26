from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- CORS yahan import kiya hai
from sqlalchemy.orm import Session
from typing import List

# Import your database, models, and schemas
from database import engine, get_db
import models
import schemas

# Create all database tables (runs when the app starts)
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="DevSetu API", description="Backend for the DevSetu platform")

# --- CORS Middleware Setup (CORS error fix karne ke liye) ---
origins = [
    "http://localhost:3000",  # Aapka local frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Welcome to the DevSetu API!"}

# --- User Routes ---
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.github_handle == user.github_handle).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="GitHub handle already registered")
    
    # Create new user
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# --- Project Routes ---
@app.post("/projects/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@