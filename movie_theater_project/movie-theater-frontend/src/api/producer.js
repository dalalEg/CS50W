import { api } from './axios';

// src/api/booking.js
export function fetchProducerById(producerId) {
  return api.get(`/api/producers/${producerId}/`);
}
export function fetchMoviesByProducer(producerId) {
  return api.get(`/api/producers/${producerId}/movies/`);
}