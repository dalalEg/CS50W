import React, { useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { createBooking } from '../api/booking';
import { useNotifications } from '../contexts/NotificationContext';

// Booking component to confirm and finalize a booking
// This component is responsible for displaying the booking confirmation page
// and handling the booking creation process.
import '../styles/Booking.css';
export default function Booking() {
  const { state }    = useLocation();
  const navigate     = useNavigate();
  const [error, setError]           = useState(null);
  const [bookingResult, setBooking] = useState(null);
  const [loading, setLoading]       = useState(false);
  const { reload: reloadNotifs } = useNotifications();
  const showtimeId = state?.showtimeId;
  const seats      = state?.seats      || [];
  if (!showtimeId || !seats.length) {
    return (
      <div className="booking-confirm">
        <p>No booking in progress.</p>
        <Link to="/">← Back to home</Link>
      </div>
    );
  }

  const totalCost = seats.reduce((sum, seat) => sum + Number(seat.price), 0);

const handleConfirm = async e => {
  e.preventDefault();
  if (loading) return;
  setLoading(true);
  const seatIds = seats.map(s => s.id);
  createBooking(showtimeId, seatIds)
    .then(resp => setBooking(resp.data))
    .then(() => reloadNotifs())
    .catch(err => {
      const status = err.response?.status;
      
      if (status === 401 || status === 403) {
        setError('Please log in to place a booking. If you\'re already logged in, please verify your email address.');
        return;
      }
      const data = err.response?.data || {};
      const fieldErrors = [];
      if (data.seat_ids)      fieldErrors.push(...data.seat_ids);
      if (data.showtime_id)   fieldErrors.push(...data.showtime_id);
      if (data.detail)        fieldErrors.push(data.detail);
      setError(fieldErrors.length
        ? fieldErrors.join(', ')
        : 'Failed to place booking.'
      );
    })
    .finally(() => setLoading(false));
};

  return (
    <div className="booking-confirm container mt-4">
      <h2>Confirm Your Booking</h2>

      <table className="table">
        <thead>
          <tr><th>Seat</th><th>Price</th></tr>
        </thead>
        <tbody>
          {seats.map(s => (
            <tr key={s.id}>
              <td>{s.seat_number}</td>
              <td>${s.price}</td>
            </tr>
          ))}
          <tr className="table-active">
            <td><strong>Total Cost:</strong></td>
            <td><strong>${totalCost}</strong></td>
          </tr>
        </tbody>
      </table>

      {error && <p className="text-danger">{error}</p>}

      {!bookingResult && (
        <div className="d-flex gap-2">
          <button
            type="button"               
            className="btn btn-primary"
            onClick={handleConfirm}
            disabled={loading}
          >
            {loading ? 'Booking…' : 'Confirm Booking'}
          </button>

          <button
            type="button"              
            className="btn btn-secondary"
            onClick={() => navigate(-1)}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      )}
        {bookingResult && ( 
            <div className="alert alert-success mt-3">
                <h4>Booking Successful!</h4>
                <p>Booking ID: <strong>{bookingResult.id}</strong></p>
                <p>Total Cost: <strong>${bookingResult.cost}</strong></p>
                <Link to={`/bookings/${bookingResult.id}`}
                  state={{ booking: bookingResult.id }}
                >View Booking Details</Link>
            </div>
        )}
      <Link to={`/showtimes/${showtimeId}`} className="btn btn-link mt-3">
        ← Back to Showtime Details
      </Link>
    </div>
  );
}