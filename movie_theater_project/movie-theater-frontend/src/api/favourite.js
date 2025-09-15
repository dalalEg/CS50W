import { api,fetchCSRFToken } from './axios';

export const fetchFavoritesByMovie = movieId =>
  api.get(`/api/favorites/?movie=${movieId}`);

export const createFavorite = async movieId => {
  await fetchCSRFToken();
  return await api.post(`/api/favorites/`, { movie: movieId });
};

export const deleteFavorite = async id => {
  await fetchCSRFToken();
  return await api.delete(`/api/favorites/${id}/`);
};