import React, { useState, useEffect } from 'react';

const AdminPanel = () => {
    const [movies, setMovies] = useState([]);
    const [showtimes, setShowtimes] = useState([]);

    useEffect(() => {
        fetchMovies();
        fetchShowtimes();
    }, []);

    const fetchMovies = async () => {
        const response = await fetch('/api/movies/');
        const data = await response.json();
        setMovies(data);
    };

    const fetchShowtimes = async () => {
        const response = await fetch('/api/showtimes/');
        const data = await response.json();
        setShowtimes(data);
    };

    const handleAddMovie = async (newMovie) => {
        const response = await fetch('/api/movies/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newMovie),
        });
        if (response.ok) {
            fetchMovies();
        }
    };

    const handleDeleteMovie = async (movieId) => {
        const response = await fetch(`/api/movies/${movieId}/`, {
            method: 'DELETE',
        });
        if (response.ok) {
            fetchMovies();
        }
    };

    return (
        <div>
            <h1>Admin Panel</h1>
            <h2>Manage Movies</h2>
            <ul>
                {movies.map(movie => (
                    <li key={movie.id}>
                        {movie.title}
                        <button onClick={() => handleDeleteMovie(movie.id)}>Delete</button>
                    </li>
                ))}
            </ul>
            {/* Add movie form and other admin functionalities can be added here */}
        </div>
    );
};

export default AdminPanel;