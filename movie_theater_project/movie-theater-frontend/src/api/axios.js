import axios from 'axios';
import Cookies from 'js-cookie';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,   // critical for cross-origin cookies
  headers: { 'Content-Type': 'application/json' },  // Removed 'X-CSRFToken' line
});

// CSRF Interceptor: Set X-CSRFToken header dynamically for every request
api.interceptors.request.use((config) => {
  const csrfToken = Cookies.get('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

api.defaults.xsrfCookieName = 'csrftoken';
api.defaults.xsrfHeaderName = 'X-CSRFToken';

// Fetch CSRF token before first request (still useful for initial setup)
export const fetchCSRFToken = async () => {
  const res = await api.get("/csrf/");  // calls backend /csrf/ endpoint
  const token = res.data.csrfToken;
  // No need to set manually anymore—interceptor handles it
  return token;
};
