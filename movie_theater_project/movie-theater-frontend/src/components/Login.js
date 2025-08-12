import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { api } from '../api/axios';    // your axios instance
import 'bootstrap/dist/css/bootstrap.min.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError]       = useState('');
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    try {
      const res = await api.post('/api/auth/login/', { username, password });
      onLogin(res.data);  // Call the onLogin prop with user data   
      navigate('/');         // back to home
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="card shadow p-4" style={{ minWidth: '300px', maxWidth: '500px', width: '100%' }}>
        <div className="card-body">
          <h2 className="card-title text-center mb-3">Login</h2>
          <p className="text-center">
            Welcome to Dali Movie Theater management system. Please log in to continue.
          </p>

          {error && <div className="alert alert-danger">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <input
                autoFocus
                className="form-control"
                type="text"
                placeholder="Username"
                value={username}
                onChange={e => setUsername(e.target.value)}
                autoComplete='username'
              />
            </div>
            <div className="form-group mb-3">
              <input
                className="form-control"
                type="password"
                placeholder="Password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                autoComplete='current-password'
              />
            </div>
            <button className="btn btn-primary w-100" type="submit">
              Login
            </button>
          </form>

          <div className="text-center mt-3">
            Don’t have an account? <Link to="/register">Register here</Link>.
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;