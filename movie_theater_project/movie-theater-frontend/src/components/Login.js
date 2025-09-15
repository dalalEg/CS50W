import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth }    from '../contexts/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';

function Login({ onLogin }) {
  const { login }         = useAuth();
  const [username, setUsername]  = useState('');
  const [password, setPassword]  = useState('');
  const [error, setError] = useState('');
  const nav               = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const response = await login({ username, password });
      console.log('Login successful:', response);
      nav('/');
    } catch (err) {
      console.error('Login failed:', err);
      setError('Login failed');
      setTimeout(() => setError(''), 3000);
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