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

 const login = async (username, password) => {
  try {
    await fetchCSRFToken();  // Ensure initial token
    const response = await api.post('/api/auth/login/', { username, password });
    
    // ✅ Update CSRF token from response
    if (response.data.csrfToken) {
      Cookies.set('csrftoken', response.data.csrfToken, { secure: true, sameSite: 'None' });
    }
    
    const userResponse = await api.get('/api/auth/user/');
    setUser(userResponse.data);
  } catch (error) {
    console.error('Login failed:', error);
  }
};

const logout = async () => {
  try {
    await api.post('/api/auth/logout/');
  } catch (error) {
    console.error('Logout failed:', error);
  } finally {
    // Always clear cookies and user state
    setUser(null);
    Cookies.remove('csrftoken');
    Cookies.remove('sessionid');
  }
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



  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}