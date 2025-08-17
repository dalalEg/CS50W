import { api } from './axios';

export const fetchServiceReviews = bookingID =>
  api.get(`/api/rate-services/?booking=${bookingID}`);


export const createServiceReview = (bookingId, payload) =>
  api.post('/api/rate-services/', {
    booking_id:     bookingId,
    all_rating:      payload.all_rating,
    show_rating:     payload.show_rating,
    auditorium_rating: payload.auditorium_rating,
    comment:         payload.comment||''
  });