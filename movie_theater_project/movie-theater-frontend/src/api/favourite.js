import { api } from './axios';

export const fetchFavoritesByMovie = movieId =>
  api.get(`/api/favorites/?movie=${movieId}`);

export const createFavorite = movieId =>
  api.post(`/api/favorites/`, { movie: movieId });

export const deleteFavorite = id =>
  api.delete(`/api/favorites/${id}/`);