import { api } from './axios';

// src/api/booking.js
export function createBooking(showtimeId, seatIds) {
  return api.post('/api/bookings/', {
    showtime_id:  showtimeId,
    seat_ids:  seatIds    
  });
}

  export const fetchBookingById = (bookingId) =>
  api.get(`/api/bookings/${bookingId}/`);
export const fetchBookingsByUser = () =>
  api.get('/api/bookings/user/');
export const cancelBooking = (bookingId) =>
  api.delete(`/api/bookings/${bookingId}/`);
export const fetchBookingDetails = (bookingId) =>
  api.get(`/api/bookings/${bookingId}/details/`);