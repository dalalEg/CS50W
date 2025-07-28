import React, { useEffect, useState } from 'react';

const MovieList = () => {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        const fetchMovies = async () => {
            const response = await fetch('/api/movies/');
            const data = await response.json();
            setMovies(data);
        };

        fetchMovies();
    }, []);

    return (
        <div className="movie-list">
            <h2>Available Movies</h2>
            <ul>
                {movies.map(movie => (
                    <li key={movie.id}>
                        <h3>{movie.title}</h3>
                        <p>{movie.description}</p>
                        <p>Showtimes: {movie.showtimes.join(', ')}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MovieList;