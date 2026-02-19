from sqlalchemy import Column, Integer, String, Text, Enum, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# This creates a "users" table in your MySQL database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # This links user to their tasks (one user can have many tasks)
    tasks = relationship("Task", back_populates="owner")


# This creates a "tasks" table in your MySQL database
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum("todo", "in_progress", "completed"), default="todo")
    priority = Column(Enum("low", "medium", "high"), default="medium")
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # This links each task to a user
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")