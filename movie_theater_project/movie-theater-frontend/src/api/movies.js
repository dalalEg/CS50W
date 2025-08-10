// src/api/movies.js
import { api} from './axios';

export const fetchMovies = () => api.get('/api/movies/');
export const fetchMovieById  = id => api.get(`/api/movies/${id}/`);
export const fetchMovieByActor = actorId => api.get(`/api/actors/${actorId}/movies/`);
export const fetchMovieByDirector = directorId => api.get(`/api/directors/${directorId}/movies/`);
export const fetchMovieByProducer = producerId => api.get(`/api/producers/${producerId}/movies/`);