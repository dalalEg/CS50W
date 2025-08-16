import React, { useState, useEffect } from 'react';
import { useNavigate, Link, useParams } from 'react-router-dom';
import { fetchBookingById, cancelBooking, updateBooking } from '../api/booking';
import { fetchAvailableSeats } from '../api/seats';
import '../styles/BookingDetail.css';

export default function BookingDetail() {
  const { bookingId } = useParams();
  const navigate = useNavigate();

  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editing, setEditing] = useState(false);
  const [selectedSeatIds, setSelectedSeatIds] = useState([]);
  const [availableSeats, setAvailableSeats] = useState([]);

  // Load booking
  useEffect(() => {
    if (!bookingId) { setLoading(false); return; }
    (async () => {
      try {
        const resp = await fetchBookingById(bookingId);
        setBooking(resp.data);
      } catch {
        setError('Error fetching booking.');
      } finally {
        setLoading(false);
      }
    })();
  }, [bookingId]);

  // Load seats for editing
  useEffect(() => {
    if (editing && booking) {
      // Initialize with current booked seats
      setSelectedSeatIds(booking.seats.map(s => s.id));

      fetchAvailableSeats(booking.showtime.id)
        .then(resp => setAvailableSeats(resp.data))
        .catch(() => setError('Error fetching available seats.'));
    }
  }, [editing, booking]);

  if (loading) return <div>Loading…</div>;
  if (error) return <div className="text-danger">{error}</div>;
  if (!booking) return <div>No booking found.</div>;

  const canCancel = new Date(booking.showtime.start_time) > new Date();
  const canEdit = editing && canCancel;

  const editableSeats = editing
    ? [
        ...booking.seats,
        ...availableSeats.filter(a => !booking.seats.some(s => s.id === a.id))
      ]
    : [];

  const handleCancel = async () => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) return;
    try {
      await cancelBooking(booking.id);
      navigate('/bookings');
    } catch {
      setError('Failed to cancel booking.');
    }
  };

  const handleEdit = async () => {
    if (selectedSeatIds.length === 0) {
      alert('You must select at least one seat.');
      return;
    }
    try {
      const resp = await updateBooking(booking.id, selectedSeatIds);
      setBooking(resp.data);
      setEditing(false);
    } catch (err) {
      console.error(err.response?.data || err.message);
      setError('Failed to update booking.');
    }
  };

  return (
    <div className="booking-detail">
      <h2>Booking Details</h2>
      <p>Movie: {booking.showtime.movie.title}</p>
      <p>Start: {new Date(booking.showtime.start_time).toLocaleString()}</p>
      <p>End: {new Date(booking.showtime.end_time).toLocaleString()}</p>
      <p>Seats: {booking.seats.map(s => `${s.seat_number} ($${s.price})`).join(', ')}</p>
      <p>Total Price: ${booking.cost}</p>
      <p>Status: {booking.status}</p>

      {editing ? (
        <div className="edit-form">
          <h3>Edit Seats</h3>
          {editableSeats.map(seat => (
            <label key={seat.id} style={{ display:'block', margin:'.5rem 0' }}>
              <input
                type="checkbox"
                value={seat.id}
                checked={selectedSeatIds.includes(seat.id)}
                disabled={new Date(booking.showtime.start_time) <= new Date()}
                onChange={e => {
                  const sid = parseInt(e.target.value, 10);
                  setSelectedSeatIds(sel =>
                    e.target.checked
                      ? [...sel, sid]
                      : sel.filter(id => id !== sid)
                  );
                }}
              />{' '}
              {seat.seat_number} (${seat.price})
            </label>
          ))}
          <button className="btn btn-primary" onClick={handleEdit}>Save</button>
          <button className="btn btn-secondary ms-2" onClick={() => setEditing(false)}>Cancel</button>
        </div>
      ) : (
        canCancel && (
          <button className="btn btn-secondary" onClick={() => setEditing(true)}>
            Edit Booking
          </button>
        )
      )}

      {canCancel && (
        <button className="btn btn-danger ms-2" onClick={handleCancel}>Cancel Booking</button>
      )}
      {!canCancel && <p className="text-muted">Cannot cancel past bookings.</p>}

      <p>Created At: {new Date(booking.created_at).toLocaleString()}</p>
      <button onClick={() => navigate(-1)} className='btn btn-secondary mt-2'>Back to Bookings</button>
    </div>
  );
}
