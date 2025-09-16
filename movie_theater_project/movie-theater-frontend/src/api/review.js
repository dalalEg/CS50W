import { api, fetchCSRFToken } from './axios';

// src/api/booking.js
export async function createReview(movieId, { content, rating, anonymous }) {
  await fetchCSRFToken();
  return await api.post(`/api/movies/${movieId}/reviews/`, {
    content,
    rating,
    anonymous,
    movie_id: movieId
  });
}
export function fetchReviewsByMovie(movieId) {
  return api.get(`/api/movies/${movieId}/reviews/`);
}
export function fetchReviewsByUser(userId, page = 1, pageSize = 10) {
  return api.get(`/api/reviews/?user=${userId}&page=${page}&page_size=${pageSize}`);
}

export async function handleDeleteReview(reviewId) {
  await fetchCSRFToken();
  return await api.delete(`/api/reviews/${reviewId}/`);
}
export async function handleUpdateReview(reviewId, { content, rating, anonymous }) {
  await fetchCSRFToken();
  return await api.patch(`/api/reviews/${reviewId}/`, {
    content,
    rating,
    anonymous
  });
}