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
