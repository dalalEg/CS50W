import { api,fetchCSRFToken } from './axios';

// GET list filtered by user id
export const fetchWatchlistByUser = userId =>
  api.get(`/api/watchlist/?user=${userId}`);

// POST to create a new entry (user is implicit via perform_create)
export const addToWatchlist = async movieId => {
  await fetchCSRFToken();
  return await api.post(`/api/watchlist/`, { movie_id: movieId });
};

// DELETE by the watchlist‐item’s own ID
export const removeFromWatchlist = async watchlistId => {
  await fetchCSRFToken();
  return await api.delete(`/api/watchlist/${watchlistId}/`);
};
