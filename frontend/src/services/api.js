import axios from 'axios'

const API_URL = 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to every request if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export const register = async (userData) => {
    const response = await axios.post('/register', userData)
    return response.data
}

export const login = async(credentials) => {
    const response = await axios.post('/login', credentials)
    if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
    }
    return response.data
}

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

export const getCurrentUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};


// ──────────────────────────────────────────────
// TASK FUNCTIONS
// ──────────────────────────────────────────────

export const getTasks = async (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.status) params.append('status_filter', filters.status);
  if (filters.priority) params.append('priority_filter', filters.priority);
  
  const response = await api.get(`/tasks?${params.toString()}`);
  return response.data;
};

export const createTask = async (taskData) => {
  const response = await api.post('/tasks', taskData);
  return response.data;
};

export const updateTask = async (taskId, taskData) => {
  const response = await api.put(`/tasks/${taskId}`, taskData);
  return response.data;
};

export const deleteTask = async (taskId) => {
  const response = await api.delete(`/tasks/${taskId}`);
  return response.data;
};

export default api;