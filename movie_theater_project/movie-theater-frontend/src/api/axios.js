import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,   // critical for cross-origin cookies
  headers: { 'Content-Type': 'application/json' },
});

// Fetch CSRF token before first request
export const fetchCSRFToken = async () => {
  const res = await api.get("/csrf/");  // calls backend /csrf/ endpoint
  const token = res.data.csrfToken;
  api.defaults.headers['X-CSRFToken'] = token;
  return token;
};
