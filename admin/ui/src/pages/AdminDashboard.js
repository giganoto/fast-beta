import React from 'react';
import useAuth from '../hooks/useAuth';

const AdminDashboard = () => {
  const { isAuth, handleLogin, handleLogout } = useAuth();

  return (
    <>
      <header>
        <nav>
          <ul>
            <li>
              {isAuth ? (
                <button className="primary-btn" onClick={handleLogout}>Logout</button>
              ): (
                <button className="primary-btn" onClick={handleLogin}>Login</button>
              )}
            </li>
          </ul>
        </nav>
      </header>
      <main>
        <h1>{ isAuth ? "Admin Dashboard" : "Please Login" }</h1>
      </main>
      <footer></footer>
    </>
  );
}

export default AdminDashboard;