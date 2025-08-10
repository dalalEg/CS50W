import { api } from './axios';

// src/api/booking.js
export function fetchDirectorById(directorId) {
  return api.get(`/api/directors/${directorId}/`);
}

export function fetchDirectors() {
  return api.get('/api/directors/');
} 