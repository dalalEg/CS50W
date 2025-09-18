import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, fetchCSRFToken } from '../api/axios';
import Cookies from 'js-cookie';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

// Detect environment for samesite
const isProduction = window.location.protocol === 'https:';
const SAMESITE = isProduction ? 'None' : 'Lax';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        await fetchCSRFToken();  // Ensure CSRF token
        const response = await api.get('/api/auth/user/');
        setUser(response.data);
      } catch (error) {
        // console.error('Failed to fetch user:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const login = async ({ username, password }) => {
    try {
      await fetchCSRFToken();  // Fetch CSRF before login
      // console.log('Attempting login for:', username);
      const response = await api.post('/api/auth/login/', { username, password });
      // console.log('Login response:', response);

      // Update CSRF token if provided by backend
      if (response.data.csrfToken) {
        // Use document.cookie for reliable setting
        document.cookie = `csrftoken=${response.data.csrfToken}; path=/; secure=${isProduction}; samesite=${SAMESITE}`;
      }

      // Fetch user profile after login
      const userResponse = await api.get('/api/auth/user/');
      // console.log('User fetched:', userResponse.data);
      setUser(userResponse.data);
      return { success: true };
    } catch (error) {
      // console.error('Login failed:', error.response?.data || error.message);
      throw error;  // Re-throw for component handling
    }
  };

  const register = async (data) => {
    try {
      await fetchCSRFToken();  // Fetch CSRF before register
      // console.log('Attempting register for:', data.username);
      
      // Exclude 'confirmation' from the data sent to backend
      const { confirmation, ...registerData } = data;
      // console.log('Sending data:', registerData);  // Debug: Log what's actually sent

      // Send as FormData instead of JSON for better compatibility
      const formData = new FormData();
      formData.append('username', registerData.username);
      formData.append('email', registerData.email);
      formData.append('password', registerData.password);
      
      const response = await api.post('/api/auth/register/', formData);
      // console.log('Register response:', response);
      // console.log('Response data:', response.data);  // Debug: Log backend response

      // Update CSRF token if provided by backend
      if (response.data.csrfToken) {
        document.cookie = `csrftoken=${response.data.csrfToken}; path=/; secure=${isProduction}; samesite=${SAMESITE}`;
      }

      // Fetch user profile after register
      const userResponse = await api.get('/api/auth/user/');
      setUser(userResponse.data);
      return { success: true };
    } catch (error) {
      // console.error('Register failed:', error.response?.data || error.message);
      // console.error('Full error:', error);  // Debug: Log full error
      throw error;
    }
  };
  const logout = async () => {
    try {
      await fetchCSRFToken();  // Fetch CSRF before logout
      await api.post('/api/auth/logout/');
      // console.log('Logout successful');
    } catch (error) {
      // console.error('Logout failed:', error);
    } finally {
      // Always clear state and cookies
      setUser(null);
      Cookies.remove('csrftoken');
      Cookies.remove('sessionid');
      window.location.href = '/';  // Force redirect
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}