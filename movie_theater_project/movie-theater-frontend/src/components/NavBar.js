import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext';
import { useNotifications } from '../contexts/NotificationContext';
import '../styles/NavBar.css';
export default function NavBar() {
  const { user, logout } = useAuth();
  const { notes }      = useNotifications();
  const unreadCount    = notes.filter(n => !n.is_read).length;
  return (
        <nav className="navbar">
            <Link to="/" className="navbar-link">All Movies</Link>
            <Link to="/showtimes" className="navbar-link">Available Showtimes</Link>
            <Link to="/theaters" className="navbar-link">Our Theaters</Link>

        {!user && (
            <>
            <Link to="/login"    className="navbar-link">Login</Link>
            <Link to="/register" className="navbar-link">Register</Link>
            </>
        )}

        {user && (
            <>
            <Link to="/profile" className="navbar-link">Profile</Link>
            <div className="notif-icon">
                
                <Link to="/notifications" className="navbar-link">🔔
                {unreadCount > 0 && <span className="badge">{unreadCount}</span>}</Link>
            </div>
            <button onClick={logout} className="navbar-link">
                Logout
            </button>
            </>
        )}
    </nav>
    )
}

