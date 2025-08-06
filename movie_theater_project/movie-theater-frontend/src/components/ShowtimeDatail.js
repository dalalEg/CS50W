import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchShowtimeById } from '../api/showtimes';
import { fetchSeats } from '../api/seats';
import { createBooking } from '../api/booking';
import './ShowtimeDetail.css';

function ShowtimeDetail() {
  const { id } = useParams();
  const [showtime, setShowtime] = useState(null);
  const [seats, setSeats] = useState([]);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [error, setError] = useState(null);

  const onSeatSelect = (selected) => setSelectedSeats(selected);

  useEffect(() => {
    fetchShowtimeById(id)
      .then(resp => setShowtime(resp.data))
      .catch(() => setError("Failed to load showtime details"));
  }, [id]);

  useEffect(() => {
    fetchSeats(id)
      .then(res => setSeats(res.data))
      .catch(err => console.error("Error loading seats", err));
  }, [id]);

  const toggleSelect = (seat) => {
    if (seat.is_booked) return;

    const updated = selectedSeats.includes(seat.id)
      ? selectedSeats.filter(id => id !== seat.id)
      : [...selectedSeats, seat.id];

    setSelectedSeats(updated);
    onSeatSelect(updated);
  };

  const handleBooking = () => {
    createBooking(id, selectedSeats)
      .then(() => {
        alert(`Successfully booked ${selectedSeats.length} seat(s)!`);
        fetchSeats(id).then(r => setSeats(r.data));
        setSelectedSeats([]);
      })
      .catch(() => setError('Booking failed'));
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

      <div className="seat-section">
        <h4 className="mb-2">Select Your Seats</h4>
        <div className="seat-map">
          {seats.map(seat => (
            <button
              key={seat.id}
              className={`seat ${seat.is_booked ? 'booked' : selectedSeats.includes(seat.id) ? 'selected' : 'available'}`}
              onClick={() => toggleSelect(seat)}
              disabled={seat.is_booked}
            >
              {seat.seat_number}
              <br />
              <span className="seat-price">${seat.price}</span>
            </button>
          ))}
        </div>
        <div className="mt-3">
          <button
            className="btn btn-primary"
            disabled={selectedSeats.length === 0}
            onClick={handleBooking}
          >
            Book {selectedSeats.length} Seat{selectedSeats.length !== 1 && 's'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ShowtimeDetail;
