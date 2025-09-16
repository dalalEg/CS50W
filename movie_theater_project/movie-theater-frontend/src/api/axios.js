import axios from 'axios';
import Cookies from 'js-cookie';

// Detect environment for samesite
const isProduction = window.location.protocol === 'https:';
const SAMESITE = isProduction ? 'None' : 'Lax';

const api = axios.create({
  baseURL: isProduction
    ? 'https://movie-theater-dots.onrender.com'
    : 'http://localhost:8000',
  withCredentials: true,
});

// Fetch and set CSRF token
export const fetchCSRFToken = async () => {
  try {
    const response = await api.get('/csrf/');
    // Use document.cookie for reliable setting
    document.cookie = `csrftoken=${response.data.csrfToken}; path=/; secure=${isProduction}; samesite=${SAMESITE}`;
  } catch (error) {
    console.error('Failed to fetch CSRF token:', error);
  }
};

// Interceptor to add CSRF token to requests
api.interceptors.request.use(
  (config) => {
    const csrfToken = Cookies.get('csrftoken');
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export { api };
