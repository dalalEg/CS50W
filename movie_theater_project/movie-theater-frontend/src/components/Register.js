import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth }    from '../contexts/AuthContext';
import { useNotifications } from '../contexts/NotificationContext';

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmation: ''
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { register } = useAuth();
  const { add: addNotif } = useNotifications();

  const handleChange = e => {
    setFormData(f => ({ ...f, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async e => {
      e.preventDefault();
      if (formData.password !== formData.confirmation) {
        setMessage("Passwords don't match");
        return;
      }
      try {
        await register(formData);
        addNotif('Welcome ' + formData.username +'! Please Confirm Your Email Address To get started.');
        navigate('/');
      } catch {
        setMessage('Registration failed');
      }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="card shadow p-4" style={{minWidth:'300px', maxWidth:'500px', width:'100%'}}>
        <div className="card-body">
          <h2 className="card-title text-center mb-3">Register</h2>
          {message && <div className="alert alert-danger">{message}</div>}

          <form onSubmit={handleSubmit}>
            <input
              name="username"
              autoComplete="username"
              className="form-control mb-3"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              required
            />
            <input
              name="email"
              type="email"
              autoComplete="email"
              className="form-control mb-3"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <input
              name="password"
              type="password"
              autoComplete="new-password"
              className="form-control mb-3"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <input
              name="confirmation"
              type="password"
              autoComplete="new-password"
              className="form-control mb-3"
              placeholder="Confirm Password"
              value={formData.confirmation}
              onChange={handleChange}
              required
            />
            <button className="btn btn-primary w-100" type="submit">
              Register
            </button>
          </form>

          <div className="text-center mt-3">
            Already have an account? <Link to="/login">Login here</Link>.
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;