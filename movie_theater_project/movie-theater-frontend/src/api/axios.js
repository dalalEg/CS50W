import axios from 'axios';
import Cookies from 'js-cookie';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,   // critical for cross-origin cookies
  headers: { 'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken'),
  },

});
api.defaults.xsrfCookieName = 'csrftoken';
api.defaults.xsrfHeaderName = 'X-CSRFToken';

// Fetch CSRF token before first request
export const fetchCSRFToken = async () => {
  const res = await api.get("/csrf/");  // calls backend /csrf/ endpoint
  const token = res.data.csrfToken;
  api.defaults.headers['X-CSRFToken'] = token;
  return token;
};
