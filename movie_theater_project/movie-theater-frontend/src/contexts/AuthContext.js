import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/axios';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(null);
  const [loading, setLoading] = useState(true);

  // on mount, fetch profile (if session cookie present)
  useEffect(() => {
    api.get('/api/auth/user/')
      .then(r => setUser(r.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = async ({ username, password }) => {
    await api.post('/api/auth/login/', { username, password });
    const r = await api.get('/api/auth/user/');
    setUser(r.data);
  };

  const register = async data => {
    const res = await api.post('/api/auth/register/', data);
    if (res.status === 200 || res.status === 201) {
      setUser(res.data.user);
  }

  };

  const logout = async () => {
    await api.post('/api/auth/logout/');
    // navigate to login page
    window.location.href = '/';
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}