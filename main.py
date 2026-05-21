from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/projects/", response_model=List[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()