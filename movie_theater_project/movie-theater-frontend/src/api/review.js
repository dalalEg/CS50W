import { api } from './axios';

// src/api/booking.js
export function createReview(movieId, { content, rating }) {
  return api.post(`/api/movies/${movieId}/reviews/`, {
    content,
    rating
  });
}
export function fetchReviewsByMovie(movieId) {
  return api.get(`/api/movies/${movieId}/reviews/`);
}