import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchCurrentUser, apiLogin } from '../api/user';
import { api } from '../api/axios';    // your axios instance
const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(null);
  const [loading, setLoading] = useState(true);
  
  // 1) on app mount, fetch current user if any
  useEffect(() => {
    fetchCurrentUser()
      .then(res => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);
  // NEW: register & immediately set user in context
  const register = async ({ username, email, password, confirmation }) => {
    await api.post('/api/auth/register/', {
      username,
      email,
      password,
      confirmation
    });
    // fetch the newly-created user profile
    const resp = await api.get('/api/auth/user/');
    setUser(resp.data);
  };


  return (
    <AuthContext.Provider value={{ user, loading, register }}>
      {children}
    </AuthContext.Provider>
  );
}