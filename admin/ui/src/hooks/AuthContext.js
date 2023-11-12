import { createContext } from 'react';

export const AuthContext = createContext({
  isAuth: false, // Initial state
  handleLogin: () => {},
  handleLogout: () => {}
});