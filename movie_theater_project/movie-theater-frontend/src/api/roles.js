import { api } from './axios';

// src/api/booking.js
export function fetchRolesByMovie(movieId) {
  return api.get(`/api/movies/${movieId}/roles/`);
}
export function fetchRole(roleId) {
  return api.get(`/api/roles/${roleId}/`);
}