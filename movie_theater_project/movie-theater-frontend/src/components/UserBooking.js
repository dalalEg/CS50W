import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { fetchBookingsByUser } from "../api/booking";
import { useAuth } from '../contexts/AuthContext';
import '../styles/UserBooking.css';

const UserBooking = () => {
  const { user } = useAuth();
  const userId = user?.id;
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 10;  // Items per page

  useEffect(() => {
    if (!userId) {
      setBookings([]);
      setLoading(false);
      return;
    }
    fetchBookings(userId, currentPage);
  }, [userId, currentPage]);

  const fetchBookings = async (userId, page) => {
    setLoading(true);
    try {
      const response = await fetchBookingsByUser(userId, page, pageSize);
      setBookings(response.data.results || response.data);
      setTotalPages(Math.ceil((response.data.count || 0) / pageSize));
      setError(null);
    } catch {
      setError('Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  if (!user) return <p>Loading user information...</p>;
  if (loading) return <p>Loading bookings...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="user-booking">
      <h2>Your Bookings ({bookings.length} Total)</h2>
      <ul>
        {bookings.length === 0 && <p>You have no bookings yet. Click <Link to={`/showtimes`}>here</Link> to browse showtimes to book a movie.</p>}
        {bookings.map(booking => (
          <li key={booking.id}>
            <Link to={`/bookings/${booking.id}`} className="link">{booking?.showtime?.movie?.title}</Link>
            <p><strong>Showtime:</strong> {new Date(booking.showtime?.start_time).toLocaleString()}</p>
            <p><strong>Seats:</strong> {booking.seats.map(seat => seat.seat_number).join(', ')}</p>
            <p><strong>Status:</strong> {booking.status}</p>
            <p><strong>Total Cost:</strong> ${booking.cost}</p>
            <p><strong>Created At:</strong> {new Date(booking.created_at).toLocaleString()}</p>
          </li>
        ))}
      </ul>
      {/* Pagination Controls */}
      <div className="pagination">
        <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
          Previous
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
};

export default UserBooking;
