// src/api/movies.js
import { api} from './axios';

export const fetchShowtimes = () => api.get('/api/showtimes/');
export const fetchShowtime = id => api.get(`/api/showtimes/${id}/`);
export const fetchShowtimesByMovie = movieId =>
  api.get(`/api/movies/${movieId}/showtimes/`);