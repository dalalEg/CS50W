import { api} from './axios';


export const createBooking = (showtimeId, selectedSeats) =>
  api.post('/api/bookings/', {
    showtime: showtimeId,
    seat_ids: selectedSeats    // ← use `seat_ids`, not `seats`
  });