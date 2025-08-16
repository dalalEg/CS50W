import React, {useState, useEffect} from "react";
import {useParams, Link} from "react-router-dom";
import {fetchUsers} from '../api/user';
// Profile component to display user profile information
// This component fetches and displays the user's profile details such as name, email, and points.
import '../styles/Profile.css';

function Profile() {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers(userId)
      .then(resp => {
        setUser(resp.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load user profile");
        setLoading(false);
      });
  }, [userId]);

  if (error) return <p className="error">{error}</p>;
  if (!user) return <p className="error">User not found</p>;
  return (  
    <div className="profile">
      <h1>User Profile</h1>
      <p><strong>Name:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Points:</strong> {user.points}</p>
      <Link to={`/user/bookings/${user.id}`} className="link">Click To View Your Bookings</Link>
      <Link to={`/reviews/${user.id}`} className="link">Click To View Your Reviews</Link>
      <Link to={`/watchlist/${user.id}`} className="link">Click To View Your Watchlist</Link>
    </div>
  );
}

export default Profile;
