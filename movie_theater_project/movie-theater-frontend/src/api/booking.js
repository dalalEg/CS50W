import { api, fetchCSRFToken } from './axios';


// src/api/booking.js
export async function createBooking(showtimeId, seatIds) {
  await fetchCSRFToken();
  return await api.post('/api/bookings/', {
    showtime_id:  showtimeId,
    seat_ids:  seatIds    
  });
}

export const fetchBookingById = (bookingId) =>
  api.get(`/api/bookings/${bookingId}/`);
export const fetchBookingsByUser = () =>
  api.get('/api/bookings/user/');
export const cancelBooking = async (bookingId) => {
  await fetchCSRFToken();
  await api.delete(`/api/bookings/${bookingId}/`);
};
export const fetchBookingDetails = fetchBookingById;  // alias for simplicity
export const updateBooking = async (bookingId, seatIds) => {
  await fetchCSRFToken();
  return await api.patch(`/api/bookings/${bookingId}/`, { seat_ids: seatIds });
}