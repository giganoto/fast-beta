import React from 'react';
import useAuth from '../hooks/useAuth';

const AdminDashboard = () => {
  const { isAuth, handleLogin, handleLogout } = useAuth();

  return (
    <div>
      <h1>Admin Dashboard</h1>
      {isAuth ? (
        <button onClick={handleLogout}>Logout</button>
      ): (
        <button onClick={handleLogin}>Login</button>
      )}
    </div>
  );
}

export default AdminDashboard;