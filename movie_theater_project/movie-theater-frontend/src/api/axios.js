// axios.js
import axios from 'axios';
import Cookies from 'js-cookie';

const API_URL = '/api'; // <-- use relative path so Netlify proxy kicks in

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,   // session cookies go through Netlify to Render
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken'),
  }
});

api.defaults.xsrfCookieName = 'csrftoken';
api.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

api.interceptors.request.use(config => {
  const token = Cookies.get('csrftoken');
  if (token) {
    config.headers['X-CSRFToken'] = token;
  }
  return config;
});
