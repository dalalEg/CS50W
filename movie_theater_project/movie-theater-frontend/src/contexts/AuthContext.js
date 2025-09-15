import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, fetchCSRFToken } from '../api/axios';

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
  const token = await fetchCSRFToken();
  await api.post('/api/auth/login/', { username, password }, {
    headers: { 'X-CSRFToken': token }
  });
  const r = await api.get('/api/auth/user/');
  setUser(r.data);
};

const register = async (data) => {
  const token = await fetchCSRFToken();
  const res = await api.post('/api/auth/register/', data, {
    headers: { 'X-CSRFToken': token }
  });
  if (res.status === 200 || res.status === 201) setUser(res.data.user);
};

const logout = async () => {
  const token = await fetchCSRFToken();
  await api.post('/api/auth/logout/', {}, {
    headers: { 'X-CSRFToken': token }
  });
  setUser(null);
  window.location.href = '/';
};

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}