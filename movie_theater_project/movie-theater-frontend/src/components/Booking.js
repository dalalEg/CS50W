import React, { useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { createBooking } from '../api/booking';

import './Booking.css';

export default function Booking() {
  const { state } = useLocation();
  const navigate  = useNavigate();
  const { showtimeId, seats } = state || {};   // seats is an array of full seat objects

  const [error, setError]           = useState(null);
  const [bookingResult, setBooking] = useState(null);

  if (!showtimeId || !seats) {
    // guard: if somebody lands here directly
    return (
      <div className="booking-confirm">
        <p>No booking in progress.</p>
        <Link to="/">← Back to home</Link>
      </div>
    );
  }

  const totalCost = seats
  .map(seat => seat.price)
  .reduce((sum, price) => sum + Number(price), 0);

  const handleConfirm = () => {
    const seatIds = seats.map(s => s.id);
    createBooking(showtimeId, seatIds)
      .then(resp => {
        setBooking(resp.data);
      })
      .catch(() => setError("Failed to place booking"));
  };

  const handleCancel = () => navigate(-1);

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
           
  <strong>
                <td>Total Cost: </td>
                <td>
                  ${totalCost.toFixed(2)}
                </td>
              </strong>
            </tr>

        </tbody>
      </table>

      {error && <p className="text-danger">{error}</p>}
      {bookingResult ? (
        <div className="alert alert-success">
          Booking #{bookingResult.id} confirmed! Total paid: ${bookingResult.cost}.
          <br/>
          <Link to="/showtimes">← Back to Showtimes</Link>
        </div>
      ) : (
        <div className="d-flex gap-2">
          <button className="btn btn-primary" onClick={handleConfirm}>
            Confirm Booking
          </button>
          <button className="btn btn-secondary" onClick={handleCancel}>
            Cancel
          </button>
        </div>
      )}
    </div>
  );
}
