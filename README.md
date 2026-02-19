# TaskFlow - Task Management Web Application

A full-stack task management application built with React (frontend) and FastAPI (backend), with JWT authentication, CRUD operations, and advanced filtering capabilities.

# 1 Features

- User Authentication: Secure registration and login with JWT tokens
- Task Management: Create, read, update, and delete tasks
- Search Functionality / Filtering: Search tasks by title, description, status or priority
- Responsive Design: Clean, modern UI built with vanilla CSS
- Protected Routes: Dashboard accessible only to authenticated users
- Real-time Updates: Task list updates immediately after create/edit/delete operations

# 2 Tech Stack that I Used

### Frontend
- React with Vite
- React Router for navigation
- Axios for API calls
- Vanilla CSS for styling

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- MySQL database
- JWT authentication with python-jose
- Bcrypt for password hashing
- **Pydantic** for data validation

# 3  Prerequisites
Before running this project, make sure you have the following installed:

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- MySQL (v8.0 or higher)

# 4 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd taskflow-app
```

### 2. Backend Setup
```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate.bat
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and configure
# Update with your MySQL credentials
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/taskflow_db
SECRET_KEY=your_super_secret_key_change_this_1234567890
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

### 3. Database Setup
```sql
-- Open MySQL and create database
CREATE DATABASE taskflow_db;
```

### 4. Run Backend Server
```bash
# Make sure you're in the backend folder with venv activated
uvicorn main:app --reload

# Server will run on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### 5. Frontend Setup
```bash
# Open a new terminal
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend will run on http://localhost:5173

# 4  API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login (returns JWT token)
- `GET /me` - Get current user profile (protected)

### Tasks
- `GET /tasks` - Get all tasks 
- `POST /tasks` - Create new task 
- `GET /tasks/{id}` - Get specific task 
- `PUT /tasks/{id}` - Update task 
- `DELETE /tasks/{id}` - Delete task 

### Query Parameters for GET /tasks:
- `status_filter`: Filter by status (todo, in_progress, completed)
- `priority_filter`: Filter by priority (low, medium, high)

##  Security practice

- Password Hashing: Uses bcrypt for secure password storage
- JWT Authentication: Stateless authentication with token expiration
- Frontend Guards: ProtectedRoute component prevents unauthorized access
- CORS Configuration: Properly configured for frontend-backend communication
- Input Validation: Server-side validation using Pydantic schemas

##  Made by:-
**Harshad**
B.Sc Information Technology (2025)
Mumbai, Maharashtra

