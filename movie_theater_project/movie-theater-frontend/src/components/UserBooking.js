import React, {useState, useEffect} from "react";
import {useParams, Link} from "react-router-dom";
import {fetchUsers} from '../api/user';
import { fetchBookingsByUser } from "../api/booking";
import '../styles/UserBooking.css'; 
const UserBooking = () => {
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

  if (!user) return <p>Loading user information...</p>;
  return (
    <div className="user-booking">
      <h2>Bookings for {user.username}</h2>
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
    </div>
  );
};

export default UserBooking;
