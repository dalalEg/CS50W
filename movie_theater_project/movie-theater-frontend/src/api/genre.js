import { api } from './axios';

// src/api/booking.js
export function fetchGenres() {
  return api.get('/api/genres/');
}