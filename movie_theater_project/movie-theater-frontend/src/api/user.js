// src/api/movies.js
import { api ,fetchCSRFToken} from './axios';

// GET current logged in user
export function fetchCurrentUser() {
  return api.get('api/auth/user/');
}

// POST login
export async function apiLogin(creds) {
  await fetchCSRFToken();
  return await api.post('api/auth/login/', creds);
}
export async function apiRegister(data) {
  await fetchCSRFToken();
  return await api.post('api/auth/register/', data);
}
// PUT update
export async function updateUser(data) {
  await fetchCSRFToken();
  return await api.put('api/auth/user/', data);
}

// GET generate token
export function generateToken() {
  return api.get('api/auth/generate_token/');
}

// GET confirm
export function confirmEmail(uid, token) {
  return api.get(`api/confirm/${uid}/${token}/`);
}