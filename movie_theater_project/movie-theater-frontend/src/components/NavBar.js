import React from 'react'
import { Link } from 'react-router-dom'
import '../styles/NavBar.css';

export default function NavBar({ currentUser, setCurrentUser, onLogout  }) {
    return (
        <nav className="navbar">
            <Link to="/" className="navbar-link">All Movies</Link>
            <Link to="/showtimes" className="navbar-link">Available Showtimes</Link>
            <Link to="/theaters" className="navbar-link">Our Theaters</Link>

        {!currentUser && (
            <>
            <Link to="/login"    className="navbar-link">Login</Link>
            <Link to="/register" className="navbar-link">Register</Link>
            </>
        )}

        {currentUser && (
            <>
            <Link to="/profile" className="navbar-link">Profile</Link>
            <button onClick={onLogout} className="navbar-link">
                Logout
            </button>
            </>
        )}
    </nav>
    )
}

