import axios from 'axios';
import Cookies from 'js-cookie';
const API_URL = process.env.REACT_APP_API_URL; // reads from .env.local or Netlify env



export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,   // send session cookie
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken'),  // Django CSRF protection
  }
  
});

api.defaults.xsrfCookieName = 'csrftoken';
api.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
// before each request, add the CSRF token header
api.interceptors.request.use(config => {
  const token = Cookies.get('csrftoken');
  if (token) {
    config.headers['X-CSRFToken'] = token;
  }
  return config;
});
