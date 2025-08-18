import { api } from './axios';

export const processPayment = bookingId =>
  api.post('/api/payments/process/', { booking_id: bookingId });