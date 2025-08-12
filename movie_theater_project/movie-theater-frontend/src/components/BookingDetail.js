import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link, useParams } from 'react-router-dom';
import { fetchBookingById, cancelBooking } from '../api/booking';
import '../styles/BookingDetail.css';
export default function BookingDetail() {
  const { bookingId }    = useParams();
  const navigate         = useNavigate();
  const [error, setError]     = useState(null);
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!bookingId) { setLoading(false); return; }
    (async () => {
      try {
        const resp = await fetchBookingById(bookingId);
        setBooking(resp.data);
      } catch (err) {
        setError('Error fetching booking.');
      } finally {
        setLoading(false);
      }
    })();
  }, [bookingId]);

  if (loading) return <div>Loading…</div>;
  if (error)   return <div className="text-danger">{error}</div>;
  if (!booking) return <div>No booking found.</div>;

  // only allow cancelling if showtime is still in the future
  const canCancel = new Date(booking.showtime.start_time) > new Date();

  const handleCancel = async () => {
    try {
      await cancelBooking(booking.id);
      navigate('/bookings');  // or wherever your list lives
    } catch {
      setError('Failed to cancel booking.');
    }
  };

  return (
    <div className="booking-detail">
      <h2>Booking Details</h2>
      <p>Movie: {booking.showtime?.movie?.title}</p>
      <p>Start At: {new Date(booking.showtime?.start_time).toLocaleString()}</p>
      <p>End At: {new Date(booking.showtime?.end_time).toLocaleString()}</p>
      <p>Seats: {booking.seats.map(seat => seat.seat_number + ' ($' + seat.price + ')').join(', ')}</p>
      <p>Total Price: ${booking.cost}</p>
      <p>Status: {booking.status}</p>
      {canCancel && (
        <button className="btn btn-danger" onClick={handleCancel}>Cancel Booking</button>
      )}
      {!canCancel && <p className="text-muted">Cannot cancel past bookings.</p>}
      <p>Created At: {new Date(booking.created_at).toLocaleString()}</p>
      <p>Updated At: {new Date(booking.updated_at).toLocaleString()}</p>
      <button onClick={() => navigate(-1)} className='btn btn-secondary'>Back to Bookings</button>
      <Link to={`/bookings/${booking.id}/edit`} className='btn btn-secondary'>Edit Booking</Link>
    </div>
  );
}