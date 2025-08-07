import React from 'react'
import { Link } from 'react-router-dom'
import './NavBar.css';

export default function NavBar({ isAuthenticated, username, onLogout , userId }) {
    return (
        <nav className="navbar">
            <Link to="/" className="navbar-link">All Movies</Link>
            <Link to="/showtimes" className="navbar-link">Available Showtimes</Link>
            <Link to="/theaters" className="navbar-link">Our Theaters</Link>
            <div className="navbar-links">
                {isAuthenticated ? (
                    <>
                        <Link to="/profile" className="nav-link">
                            {username}
                            { userId ? ` (ID: ${userId})` : ''}
                        </Link>
                        <button className="btn btn-link" onClick={onLogout}>
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link className="nav-link" to="/login">Login</Link>
                        <Link className="nav-link" to="/register">Register</Link>
                    </>
                )}
            </div>
        </nav>
    )
}

