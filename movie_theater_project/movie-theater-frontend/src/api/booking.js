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
export const fetchBookingDetails = fetchBookingById;  // alias for simplicity
export const updateBooking = (bookingId, seatIds) =>
  api.patch(`/api/bookings/${bookingId}/`, { seat_ids: seatIds });