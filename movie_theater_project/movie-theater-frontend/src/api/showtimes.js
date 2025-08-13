// src/api/movies.js
import { api} from './axios';

export const fetchShowtimes = () => api.get('/api/showtimes/');
export const fetchShowtimeById = id => api.get(`/api/showtimes/${id}/`);
export const fetchShowtimesByMovie = movieId =>
  api.get(`/api/movies/${movieId}/showtimes/`);
export const fetchShowtimesByTheater = theaterId =>
  api.get(`/api/theaters/${theaterId}/showtimes/`);
export const fetchShowtimesByDate = date =>
  api.get(`/api/showtimes/?date=${date}`);  
export const searchShowtimes = query =>
  api.get(`/api/showtimes/?search=${query}`);