import React, { useState, useEffect } from 'react';
import { useNavigate, Link, useParams } from 'react-router-dom';
import { fetchBookingById, cancelBooking, updateBooking } from '../api/booking';
import { fetchAvailableSeats } from '../api/seats';
import ConfirmDialog from './ConfirmDialog';
import { useToast } from '../contexts/ToastContext';
import { useNotifications } from '../contexts/NotificationContext';

import {processPayment} from '../api/payment';
import '../styles/BookingDetail.css';

export default function BookingDetail() {
  const { show } = useToast();
  const [confirmCancel, setConfirmCancel] = useState(false);
  const { bookingId } = useParams();
  const navigate = useNavigate();
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editing, setEditing] = useState(false);
  const [selectedSeatIds, setSelectedSeatIds] = useState([]);
  const [availableSeats, setAvailableSeats] = useState([]);
  const { reload: reloadNotifs } = useNotifications();

  // Load booking
  const [payment, setPaying] = useState(null);
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
    const handlePayNow = async () => {
    setLoading(true);
    try {
      await processPayment(booking.id);
      await reloadNotifs();
      show('Payment successful', 'success');
      const updated = await fetchBookingById(booking.id);
      setBooking(updated.data);
    } catch {
      show('Payment failed', 'error');
    } finally {
      setLoading(false);
    }
  };
  if (loading) return <div>Loading…</div>;
  if (error) return <div className="text-danger">{error}</div>;
  if (!booking) return <div>No booking found.</div>;

  const canCancel = new Date(booking.showtime.start_time) > new Date() && booking.status !== 'Cancelled';
  const canEdit = editing && canCancel;

  const editableSeats = editing
    ? [
        ...booking.seats,
        ...availableSeats.filter(a => !booking.seats.some(s => s.id === a.id))
      ]
    : [];

   const handleCancel = async () => {
    setConfirmCancel(false);
    try {
      await cancelBooking(booking.id);
      await reloadNotifs();
      show('Booking cancelled', 'warning');
      const updated = await fetchBookingById(booking.id);
      setBooking(updated.data);
    } catch {
      show('Failed to cancel', 'error');
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
      <p>Attended: {booking.attended ? 'Yes' : 'No'}</p>
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
          {canCancel && (
            <button className="btn btn-secondary ms-2" onClick={() => setEditing(false)}>Cancel</button>
          )}
        </div>
      ) : (
        canCancel && booking.status !== 'Cancelled' && booking.status !== 'Confirmed' && (
          <button className="btn btn-secondary" onClick={() => setEditing(true)}>
            Edit Booking
          </button>
        )
      )}
{booking.status === 'Pending' && (
        <>
          <button
            onClick={handlePayNow}
            disabled={loading}
            className="btn btn-primary me-2"
          >
            {loading ? 'Processing…' : 'Pay Now'}
          </button>
          <button
            onClick={() => setConfirmCancel(true)}
            className="btn btn-danger"
          >
            Cancel Booking
          </button>
        </>
      )}
{confirmCancel && (
        <ConfirmDialog
          message="Are you sure you want to cancel this booking?"
          onYes={handleCancel}
          onNo={() => setConfirmCancel(false)}
        />
      )}
       {booking.status === 'Confirmed' && (
         <p className="text-success">✅ Paid</p>
       )}
      {booking.status === 'Cancelled' && (
        <p className="text-muted mt-3">
          This booking has  been cancelled.
        </p>
      )}
      {booking.attended && (
        <div>
          <h3>Service Review</h3>
            <div>
             
              <button
                className="btn btn-primary"
                onClick={() => navigate(`/serviceReview/${bookingId}`)}
              >
                Leave us a Review
              </button>
            </div>
          
        </div>
      )}
      <p>Created At: {new Date(booking.created_at).toLocaleString()}</p>
      <button onClick={() => navigate(-1)} className='btn btn-secondary mt-2'>Back to Bookings</button>
    </div>
  );
}
