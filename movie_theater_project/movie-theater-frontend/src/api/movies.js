// src/api/movies.js
import { api} from './axios';

export const fetchMovies = () => api.get('/api/movies/');
export const fetchMovie  = id => api.get(`/api/movies/${id}/`);