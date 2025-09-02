import React, {useState} from "react";
import { Link} from "react-router-dom";
import { useAuth }    from '../contexts/AuthContext';
import {generateToken} from '../api/user';
// Profile component to display user profile information
// This component fetches and displays the user's profile details such as name, email, and points.
import '../styles/Profile.css';

function Profile() {
  const [error, setError] = useState(null);
  const [loading] = useState(true);
  const [emailSent, setEmailSent] = useState(false);
  const { user } = useAuth();

  const handleConfirmEmail = () => {
    generateToken(user.id, user.email)
      .then(() => {
        setEmailSent(true);
        alert("Confirmation email sent!");
      })
      .catch(() => {
        alert("Failed to send confirmation email.");
        setError("Failed to send confirmation email.");
      });
  };

  if (error) return <p className="error">{error}</p>;
  if (!user) return <p className="error">User not found</p>;
  if (loading) return <p>Loading...</p>;
  return (  
    <div className="profile">
      <h1>User Profile</h1>
        <Link to={`/user/edit/${user.id}`} className="link">Click To Edit Profile</Link>
      <p><strong>Name:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email}</p>
      {!user?.email_verified && (
        <div className="alert alert-warning">
          <p>Please confirm your email to unlock all features.</p>
          <button className="btn btn-link" onClick={handleConfirmEmail}>
            Resend confirmation email
          </button>
          {emailSent && <p>Confirmation email sent!</p>}
        </div>
      )}
      <p><strong>Points:</strong> {user.points}</p>
      <Link to={`/user/bookings/${user.id}`} className="link">Click To View Your Bookings</Link>
      <Link to={`/reviews/${user.id}`} className="link">Click To View Your Reviews</Link>
      <Link to={`/watchlist/${user.id}`} className="link">Click To View Your Watchlist</Link>
    </div>
  );
}

export default Profile;
