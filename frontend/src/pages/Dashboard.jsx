import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTasks, createTask, updateTask, deleteTask, logout, getCurrentUser } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: ''
  });
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'todo',
    priority: 'medium',
    due_date: ''
  });
  
  const loadTasks = async () => {
    try {
      const data = await getTasks(filters);
      setTasks(data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading tasks:', error);
      setLoading(false);
    }
  };

  // Load user and tasks when component mounts
  useEffect(() => {
    const currentUser = getCurrentUser();
    setUser(currentUser);
    loadTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const openModal = (task = null) => {
    if (task) {
      // Editing existing task
      setEditingTask(task);
      setFormData({
        title: task.title,
        description: task.description || '',
        status: task.status,
        priority: task.priority,
        due_date: task.due_date || ''
      });
    } else {
      // Creating new task
      setEditingTask(null);
      setFormData({
        title: '',
        description: '',
        status: 'todo',
        priority: 'medium',
        due_date: ''
      });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingTask(null);
    setFormData({
      title: '',
      description: '',
      status: 'todo',
      priority: 'medium',
      due_date: ''
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingTask) {
        // Update existing task
        await updateTask(editingTask.id, formData);
      } else {
        // Create new task
        await createTask(formData);
      }
      
      closeModal();
      
      // Reload tasks
      const data = await getTasks({});
      setTasks(data);
      
    } catch (error) {
      console.error('Error saving task:', error);
      alert('Failed to save task. Please try again.');
    }
  };

  const handleDelete = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(taskId);
        
        // Reload tasks
        const data = await getTasks({});
        setTasks(data);

      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task. Please try again.');
      }
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const applyFilters = () => {
    loadTasks();
  };

  const clearFilters = () => {
    setFilters({
      status: '',
      priority: '',
      search: ''
    });
    setTimeout(() => loadTasks(), 100);
  };

  // Filter tasks by search term (client-side)
  const filteredTasks = tasks.filter(task => {
    if (filters.search) {
      return task.title.toLowerCase().includes(filters.search.toLowerCase()) ||
             (task.description && task.description.toLowerCase().includes(filters.search.toLowerCase()));
    }
    return true;
  });

  const getStatusColor = (status) => {
    switch(status) {
      case 'todo': return '#f59e0b';
      case 'in_progress': return '#3b82f6';
      case 'completed': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="navbar-content">
          <h1 className="logo">TaskFlow</h1>
          <div className="navbar-right">
            <span className="user-name">Welcome, {user?.username}</span>
            <button onClick={handleLogout} className="btn-logout">Logout</button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container">
        {/* Header Section */}
        <div className="dashboard-header">
          <h2>My Tasks</h2>
          <button onClick={() => openModal()} className="btn-create">+ Create Task</button>
        </div>

        {/* Filters Section */}
        <div className="filters">
          <input
            type="text"
            name="search"
            placeholder="Search tasks..."
            value={filters.search}
            onChange={handleFilterChange}
            className="search-input"
          />
          
          <select name="status" value={filters.status} onChange={handleFilterChange} className="filter-select">
            <option value="">All Status</option>
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>

          <select name="priority" value={filters.priority} onChange={handleFilterChange} className="filter-select">
            <option value="">All Priority</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <button onClick={applyFilters} className="btn-filter">Apply</button>
          <button onClick={clearFilters} className="btn-clear">Clear</button>
        </div>

        {/* Tasks Grid */}
        <div className="tasks-grid">
          {filteredTasks.length === 0 ? (
            <div className="no-tasks">
              <p>No tasks found. Create your first task to get started!</p>
            </div>
          ) : (
            filteredTasks.map((task) => (
              <div key={task.id} className="task-card">
                <div className="task-header">
                  <h3>{task.title}</h3>
                  <div className="task-actions">
                    <button onClick={() => openModal(task)} className="btn-edit">Edit</button>
                    <button onClick={() => handleDelete(task.id)} className="btn-delete">Delete</button>
                  </div>
                </div>
                
                {task.description && <p className="task-description">{task.description}</p>}
                
                <div className="task-meta">
                  <span className="badge" style={{ backgroundColor: getStatusColor(task.status) }}>
                    {task.status.replace('_', ' ')}
                  </span>
                  <span className="badge" style={{ backgroundColor: getPriorityColor(task.priority) }}>
                    {task.priority}
                  </span>
                </div>
                
                {task.due_date && (
                  <div className="task-date">
                    Due: {new Date(task.due_date).toLocaleDateString()}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Modal for Create/Edit Task */}
      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>{editingTask ? 'Edit Task' : 'Create New Task'}</h2>
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Title *</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  rows="3"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Status</label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({...formData, status: e.target.value})}
                  >
                    <option value="todo">To Do</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Priority</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({...formData, priority: e.target.value})}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Due Date</label>
                <input
                  type="date"
                  value={formData.due_date}
                  onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                />
              </div>

              <div className="modal-actions">
                <button type="button" onClick={closeModal} className="btn-cancel">Cancel</button>
                <button type="submit" className="btn-submit">
                  {editingTask ? 'Update Task' : 'Create Task'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;