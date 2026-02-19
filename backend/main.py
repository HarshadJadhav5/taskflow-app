from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta, date

from database import engine, get_db, Base
from models import User, Task
from schemas import (
    UserCreate, UserResponse, LoginRequest, TokenResponse,
    TaskCreate, TaskUpdate, TaskResponse
)
from auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create all tables in the database (runs when app starts)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

# ──────────────────────────────────────────────────────────────
# CORS MIDDLEWARE (Allows React to talk to FastAPI)
# ──────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React runs on port 3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)


# ──────────────────────────────────────────────────────────────
# ROOT ENDPOINT (Just to test if server is running)
# ──────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "TaskFlow API is running!"}


# ──────────────────────────────────────────────────────────────
# AUTH ENDPOINTS
# ──────────────────────────────────────────────────────────────

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user
    Steps:
    1. Check if email/username already exists
    2. Hash the password
    3. Create user in database
    4. Return user info (without password)
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash the password
    hashed_pw = hash_password(user.password)
    
    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pw
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Logs in a user
    Now uses OAuth2PasswordRequestForm which expects username field
    We treat username as email
    """
    # form_data.username will contain the email
    db_user = db.query(User).filter(User.email == form_data.username).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }


@app.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Gets the logged-in user's profile
    This is a PROTECTED route (requires token)
    """
    return current_user


# ──────────────────────────────────────────────────────────────
# TASK ENDPOINTS (CRUD Operations)
# ──────────────────────────────────────────────────────────────

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Creates a new task for the logged-in user
    """
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        owner_id=current_user.id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: str = None,
    priority_filter: str = None
):
    """
    Gets all tasks for the logged-in user
    Can filter by status and priority
    """
    query = db.query(Task).filter(Task.owner_id == current_user.id)
    
    # Apply filters if provided
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    if priority_filter:
        query = query.filter(Task.priority == priority_filter)
    
    tasks = query.all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Gets a specific task by ID
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates a task
    Only updates fields that are provided
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only provided fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.priority is not None:
        task.priority = task_update.priority
    if task_update.due_date is not None:
        task.due_date = task_update.due_date
    
    db.commit()
    db.refresh(task)
    
    return task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletes a task
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}
