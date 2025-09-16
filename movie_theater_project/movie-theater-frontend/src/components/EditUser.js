import React, {useState, useEffect} from "react";
import {useAuth} from '../contexts/AuthContext';
import { api,fetchCSRFToken } from "../api/axios";
// Profile component to display user profile information
// This component fetches and displays the user's profile details such as name, email, and points.
import '../styles/EditUser.css';

function EditUser() {
  const { user, loading } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    old_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      setFormData({ ...formData, email: user.email });
    }
  }, [user,formData]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    if (formData.new_password && formData.new_password !== formData.confirm_password) {
      setError('New passwords do not match.');
      return;
    }

    try {
      const updateData = {};
      if (formData.email !== user.email) updateData.email = formData.email;
      if (formData.new_password) {
        updateData.new_password = formData.new_password;
        updateData.old_password = formData.old_password;
      }
      await fetchCSRFToken();  // Ensure CSRF token is fetched before making the PUT request
      await api.put('/api/auth/user/', updateData);
      setMessage('Profile updated successfully!');
      // Optionally refresh user data

      window.location.reload();  // Or update AuthContext
    } catch (err) {
      setError(err.response?.data?.detail || 'Update failed.');
    }
  };

  if (loading) return <p>Loading...</p>;
  if (!user) return <p>Please log in.</p>;

  return (
    <div className="edit-user-container">
      <h2>Edit Your Profile</h2>
      <form onSubmit={handleSubmit}>
        <label>Email:</label>
        <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        
        <label>Old Password (for password change):</label>
        <input type="password" name="old_password" value={formData.old_password} onChange={handleChange} />
        
        <label>New Password:</label>
        <input type="password" name="new_password" value={formData.new_password} onChange={handleChange} />
        
        <label>Confirm New Password:</label>
        <input type="password" name="confirm_password" value={formData.confirm_password} onChange={handleChange} />
        
        <button type="submit">Update Profile</button>
      </form>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default EditUser;
