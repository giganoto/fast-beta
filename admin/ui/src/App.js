import { useState, useEffect } from 'react';

import AdminDashboard from './pages/AdminDashboard';
import { AuthContext } from './hooks/AuthContext';
import './App.css';

function App() {

  const [isAuth, setIsAuth] = useState(false);

  const handleLogin = () => {
    window.location.href = '/api/auth/login';
  }

  const handleLogout = async () => {
    setIsAuth(false);
    const token = localStorage.getItem('token');
    localStorage.removeItem('token');
    try {
      const response = await fetch(
        '/api/auth/logout',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ token })
        });
      const data = await response.json();
      window.location.href = '/';
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    const oauth2LoginCallback = async () => {
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');
      if (code) {

        window.history.replaceState({}, document.title, window.location.pathname);

        const response = await fetch(`/api/auth/login/callback?code=${code}`);
        const data = await response.json();
        localStorage.setItem('token', data.token);
        setIsAuth(true);
      } else {
        const token = localStorage.getItem('token');
        if (token) {
          setIsAuth(true);
        }
      }
    };
  
    oauth2LoginCallback();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuth, setIsAuth, handleLogin, handleLogout }}>
      <div className='app'>
        <AdminDashboard />
      </div>
    </AuthContext.Provider>
  );
}

export default App;
