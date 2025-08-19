import { api } from './axios';

// src/api/booking.js
export function createReview(movieId, { content, rating, anonymous }) {
  return api.post(`/api/movies/${movieId}/reviews/`, {
    content,
    rating,
    anonymous
  });
}
export function fetchReviewsByMovie(movieId) {
  return api.get(`/api/movies/${movieId}/reviews/`);
}
export function fetchReviewsByUser(userId) {
  return api.get(`/api/reviews/?user=${userId}`);
}

export function handleDeleteReview(reviewId) {
  return api.delete(`/api/reviews/${reviewId}/`);
}
export function handleUpdateReview(reviewId, { content, rating, anonymous }) {
  return api.patch(`/api/reviews/${reviewId}/`, {
    content,
    rating,
    anonymous
  });
}