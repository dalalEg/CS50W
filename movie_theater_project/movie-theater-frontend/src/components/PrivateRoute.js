import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth }  from '../contexts/AuthContext';

export default function PrivateRoute({ children }) {
  const { user, loading } = useAuth();
  // still checking session?
  if (loading) return <p>Loading…</p>;
  // not logged in? bounce to login
  return user ? children : <Navigate to="/login" replace />;
}