// src/api/movies.js
import { api} from './axios';

export const fetchSeats = showtimeId => api.get(`/api/showtimes/${showtimeId}/seats/`);
export const fetchSeat = (showtimeId, seatId) => api.get(`/api/showtimes/${showtimeId}/seats/${seatId}/`);
export const fetchAvailableSeats = showtimeId => api.get(`/api/showtimes/${showtimeId}/available_seats/`);