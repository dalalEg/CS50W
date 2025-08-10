import { api } from './axios';

// src/api/booking.js
export function fetchActorById(actorId) {
  return api.get(`/api/actors/${actorId}/`);
}
