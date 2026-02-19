import { Navigate } from 'react-router-dom';
import { getCurrentUser } from '../services/api';

const ProtectedRoute = ({ children }) => {
  const user = getCurrentUser();
  
  // If no user is logged in, redirect to login page
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  // If user is logged in, show the protected page
  return children;
};

export default ProtectedRoute;