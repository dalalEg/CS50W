import React, { use, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchShowtimeById } from '../api/showtimes';
import { fetchSeats } from '../api/seats';
import { useNavigate } from 'react-router-dom';
import { createBooking } from '../api/booking';
import './ShowtimeDetail.css';

function ShowtimeDetail() {
  const { id } = useParams();
  const [seats, setSeats]               = useState([]);
  const [selected, setSelected]         = useState([]);
  const [bookingResult, setBookingResult] = useState(null);
  const [error, setError]               = useState(null);
  const [showtime, setShowtime]         = useState(null);
  const navigate = useNavigate();            // ← hook at top

  useEffect(() => {
    fetchShowtimeById(id)
      .then(resp => setShowtime(resp.data))
      .catch(() => setError("Failed to load showtime details"));
  }, [id]);

  useEffect(() => {
    fetchSeats(id).then(r => setSeats(r.data));
  }, [id]);

  const toggleSelect = seat => {
    if (seat.is_booked) return;
    setSelected(sel =>
      sel.includes(seat.id) ? sel.filter(x => x !== seat.id) : [...sel, seat.id]
    );
  };

  // sum up prices
  const selectedSeatObjs = seats.filter(s => selected.includes(s.id));
  const totalCost = selectedSeatObjs
  .map(seat => seat.price)
  .reduce((sum, price) => sum + Number(price), 0); 

  const handlePrepareBooking = () => {
    if (selectedSeatObjs.length === 0) {
      setError("Please select at least one seat to book.");
      return;
    }
    navigate('/booking', {
      state: { showtimeId: id, seats: selectedSeatObjs }
    });
  };


  if (error) return <p className="error">{error}</p>;
  if (!showtime) return <p className="loading">Loading…</p>;

  return (
    <div className="showtime-detail container mt-4">
      <Link to="/showtimes" className="btn btn-secondary mb-3">← Back to Showtimes</Link>
      <h2 className="mb-3">{showtime.movie?.title}</h2>
      <div className="mb-3">
        <p><strong>Start Time:</strong> {new Date(showtime.start_time).toLocaleString()}</p>
        <p><strong>End Time:</strong> {new Date(showtime.end_time).toLocaleString()}</p>
        <p><strong>Language:</strong> {showtime.language}</p>
        <p><strong>Auditorium:</strong> {showtime.auditorium?.name}</p>
        <p><strong>Theater:</strong> {showtime.auditorium?.theater?.name}</p>
        <p><strong>Available Seats:</strong> {showtime.auditorium?.available_seats ?? 0}</p>
        <p><strong>3D:</strong> {showtime.thD_available ? 'Yes' : 'No'} | <strong>Parking:</strong> {showtime.parking_available ? 'Yes' : 'No'}</p>
      </div>

      <h4>Select Your Seats</h4>
      <div className="seat-map">
        {seats.map(seat => (
          <button
            key={seat.id}
            className={`seat ${seat.is_booked ? 'booked' : selected.includes(seat.id) ? 'selected' : 'available'}`}
            onClick={() => toggleSelect(seat)}
            disabled={seat.is_booked}
          >
            {seat.seat_number}
            <br />
            <span className="seat-price">${seat.price}</span>
          </button>
        ))}
      </div>

      {/* price table */}
      {selectedSeatObjs.length > 0 && (
        <table className="price-table">
          <thead>
            <tr><th>Seat</th><th>Price</th></tr>
          </thead>
          <tbody>
            {selectedSeatObjs.map(s => (
              <tr key={s.id}>
                <td>{s.seat_number}</td>
                <td>${s.price}</td>
              </tr>
            ))}
            <tr className="total">
              <td><strong>Total</strong></td>
              <td><strong>${totalCost}</strong></td>
            </tr>
          </tbody>
        </table>
      )}

      {/* book button */}
      <button
        className="btn btn-primary"
        disabled={selectedSeatObjs.length === 0}
        onClick={handlePrepareBooking}
      >
        Book {selectedSeatObjs.length} Seat{selectedSeatObjs.length > 1 && 's'}
      </button>

      {/* show saved booking cost */}
      {bookingResult && (
        <p className="booking-success">
          Booking #{bookingResult.id} created. Total cost: $
          {bookingResult.cost}
        </p>
      )}
    </div>
  );
}

export default ShowtimeDetail;
