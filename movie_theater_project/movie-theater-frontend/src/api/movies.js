// src/api/movies.js
import { api } from './axios';

export const fetchMovies = (page = 1) => api.get(`/api/movies/?page=${page}`);
export const fetchMoviesByPage = (page) => api.get(`/api/movies/?page=${page}`);  // Keep for consistency, or remove if redundant
export const fetchMovieById = id => api.get(`/api/movies/${id}/`);
export const fetchMovieByActor = actorId => api.get(`/api/actors/${actorId}/movies/`);
export const fetchMovieByDirector = directorId => api.get(`/api/directors/${directorId}/movies/`);
export const fetchMovieByProducer = producerId => api.get(`/api/producers/${producerId}/movies/`);
export const searchMovies = (query, page = 1) => api.get(`/api/movies/?search=${query}&page=${page}`);