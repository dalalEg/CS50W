import React, {useState, useEffect} from "react";
import {useParams, Link} from "react-router-dom";
import {fetchUsers} from '../api/user';
import { fetchBookingsByUser } from "../api/booking";
// Profile component to display user profile information
// This component fetches and displays the user's profile details such as name, email, and points.
import './Profile.css';

function Profile() {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchUsers(userId)
      .then(resp => {
        setUser(resp.data);
        return fetchBookingsByUser(userId);
      })
      .then(resp => {
        setBookings(resp.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load user profile");
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <p className="loading">Loading…</p>;
  if (error) return <p className="error">{error}</p>;
  if (!user) return <p className="error">User not found</p>;
  return (  
    <div className="profile">
      <h1>User Profile</h1>
      <p><strong>Name:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Points:</strong> {user.points}</p>
      <h2>Bookings</h2>
      {bookings.length === 0 ? (
        <p>No bookings found for this user.</p>
      ) : (
        <ul>
          {bookings.map(booking => (
            <li key={booking.id}>
              <p><strong>Booking ID:</strong> {booking.id}</p>
              <p><strong>Movie:</strong> {booking.showtime?.movie?.title || 'Unknown Movie'}</p>
              <p><strong>Start Time:</strong> {new Date(booking.showtime?.start_time).toLocaleString()}</p>
              <p><strong>Seats:</strong> {booking.seats.map(seat => seat.seat_number).join(', ')}</p>
              <Link to={`/bookings/${booking.id}`} className="booking-link">View Booking Details</Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Profile;
