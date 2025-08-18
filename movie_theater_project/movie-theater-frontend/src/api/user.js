// src/api/movies.js
import { api } from './axios';

// GET current logged in user
export function fetchCurrentUser() {
  return api.get('api/auth/user/');
}

// POST login
export function apiLogin(creds) {
  return api.post('api/auth/login/', creds);
}
export function apiRegister(data) {
  return api.post('api/auth/register/', data);
}
// PUT update
export function updateUser(data) {
  return api.put('api/auth/user/', data);
}

// GET generate token
export function generateToken() {
  return api.get('api/auth/generate_token/');
}

// GET confirm
export function confirmEmail(uid, token) {
  return api.get(`api/confirm/${uid}/${token}/`);
}