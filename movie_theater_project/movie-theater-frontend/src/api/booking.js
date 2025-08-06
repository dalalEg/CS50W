import { api} from './axios';

export const createBooking = (showtimeId, seats) =>
  api.post('/api/bookings/', { showtime: showtimeId, seats });