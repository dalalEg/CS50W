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