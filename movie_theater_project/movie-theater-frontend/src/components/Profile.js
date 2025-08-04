import React, {useState, useEffect} from "react";
import {useParams, Link} from "react-router-dom";
import {fetchUsers} from '../api/user';
import './Profile.css';

function Profile() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers()
      .then(resp => setUser(resp.data))
      .catch(() => setError("Failed to load user details"));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!user) return <p className="loading">Loading…</p>;

  return (
    <div className="profile">
      <h1>{user.name}</h1>
      <div className="info">
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Joined:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
        <p><strong>Points:</strong> {user.points}</p>
      </div>
    </div>
  );
}

export default Profile;
