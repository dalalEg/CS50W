import { api } from './axios';
// src/api/auditorium.js
export const fetchAuditoriums = () => api.get('/api/auditoriums/');
export const fetchAuditorium = id => api.get(`/api/auditoriums/${id}/`);