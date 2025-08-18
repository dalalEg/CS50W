// src/api/movies.js
import { api} from './axios';

// If you want the current logged-in user:
export function fetchUsers() {
  return api.get('/api/auth/user/');
}

// Or if you meant to fetch all users via your DRF viewset:
export function fetchUsersList() {
  return api.get('/api/users/');
}

export function updateUser(data) {
  return api.put('/api/auth/user/', data);
}
export function generateToken() {
  return api.get('/api/auth/generate_token/');
}

export function confirmEmail(uid, token) {
  return api.get(`/api/confirm/${uid}/${token}/`);
}