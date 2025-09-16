import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, fetchCSRFToken } from '../api/axios';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(null);
  const [loading, setLoading] = useState(true);

  // on mount, fetch profile (if session cookie present)
  useEffect(() => {
    (async () => { await fetchCSRFToken(); })();
    api.get('/api/auth/user/')
      .then(r => setUser(r.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = async ({ username, password }) => {
  await fetchCSRFToken();
  await api.post('/api/auth/login/', { username, password });
  // Retry fetching user profile to handle cookie delays
  let retries = 3;
  while (retries > 0) {
    try {
      const r = await api.get('/api/auth/user/');
      if (r.data && r.data.id) {
        setUser(r.data);
        console.log('Login successful, user set:', r.data);
        return;
      }
    } catch (err) {
      console.error('User fetch failed, retrying...', err);
    }
    retries--;
    await new Promise(resolve => setTimeout(resolve, 500));  // Wait 500ms
  }
  throw new Error('Failed to fetch user after login');
};

const register = async (data) => {
  await fetchCSRFToken();
  const res = await api.post('/api/auth/register/', data);
  if (res.status === 200 || res.status === 201) {
    // Similar retry for register
    const r = await api.get('/api/auth/user/');
    setUser(r.data);
  }
};

const logout = async () => {
  await fetchCSRFToken();
  await api.post('/api/auth/logout/');
  setUser(null);
  window.location.href = '/';  // Force reload to clear any cached state
};


  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}