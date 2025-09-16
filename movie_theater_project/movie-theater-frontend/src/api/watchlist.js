import { api, fetchCSRFToken } from './axios';

// GET list filtered by user id
export const fetchWatchlistByUser = (userId, page = 1, pageSize = 10) => {
  // If pageSize is large (e.g., 1000), fetch all items for checking
  const url = `/api/watchlist/?user=${userId}&page=${page}&page_size=${pageSize}`;
  return api.get(url);
};
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


