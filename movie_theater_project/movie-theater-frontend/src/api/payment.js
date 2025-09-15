import { api , fetchCSRFToken} from './axios';

export const processPayment = async bookingId => {
  await fetchCSRFToken();
  return await api.post('/api/payments/process/', { booking_id: bookingId });
};