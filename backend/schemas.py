from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# ─────────────────────────────────────────────
# USER SCHEMAS
# ─────────────────────────────────────────────

# Data we RECEIVE when user registers
class UserCreate(BaseModel):
    username: str
    email: EmailStr        # automatically validates email format
    password: str

# Data we SEND back about the user (never send password back!)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True   # allows converting database object to this schema


# ─────────────────────────────────────────────
# AUTH SCHEMAS
# ─────────────────────────────────────────────

# Data we RECEIVE when user logs in
class LoginRequest(BaseModel):
    email: str
    password: str

# Data we SEND back after successful login (the token)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# ─────────────────────────────────────────────
# TASK SCHEMAS
# ─────────────────────────────────────────────

# Data we RECEIVE when user creates a task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"
    due_date: Optional[date] = None

# Data we RECEIVE when user updates a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

# Data we SEND back about a task
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[date]
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True