import React, {useState, useEffect} from "react";
import {useParams, Link} from "react-router-dom";
import {fetchCurrentUser,updateUser} from '../api/user';
// Profile component to display user profile information
// This component fetches and displays the user's profile details such as name, email, and points.
import '../styles/Profile.css';

function EditUser() {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCurrentUser()
      .then(resp => {
        setUser(resp.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load user profile");
        setLoading(false);
      });
  }, [userId]);
    const handleUpdate = () => {
        updateUser(userId, user)
          .then(() => {
            alert("Profile updated successfully");
          })
          .catch(() => {
            alert("Failed to update profile");
          });
  };

  if (error) return <p className="error">{error}</p>;
  if (!user) return <p className="error">User not found</p>;
  return (  
    <div className="profile">
      <p><strong>Email:</strong> <input type="email" value={user.email} onChange={(e) => setUser({...user, email: e.target.value})} /></p>
      <p><strong>Password:</strong> <input type="password" value={user.password} onChange={(e) => setUser({...user, password: e.target.value})} /></p>
      <p><strong>Confirm Password:</strong> <input type="password" value={user.confirmPassword} onChange={(e) => setUser({...user, confirmPassword: e.target.value})} /></p>
      <button onClick={handleUpdate}>Update Profile</button>
    </div>
  );
}

export default EditUser;
