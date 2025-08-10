import { api } from './axios';

// src/api/booking.js
export function fetchDirectorById(directorId) {
  return api.get(`/api/directors/${directorId}/`);
}
export function fetchMoviesByDirector(directorId) {
  return api.get(`/api/directors/${directorId}/movies/`);
}   
export function fetchDirectors() {
  return api.get('/api/directors/');
} 