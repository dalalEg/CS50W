import React, { useEffect, useState } from 'react';
import { fetchMovies } from '../api/movies';
import { useNavigate }  from 'react-router-dom';
import './MovieList.css';

function MovieList() {
  const [movies, setMovies]   = useState([]);
  const [error, setError]     = useState(null);
  const navigate              = useNavigate();

  useEffect(() => {
    fetchMovies()
      .then(r => setMovies(r.data))
      .catch(() => setError("Failed to fetch movies."));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!movies.length) return <p className="loading">Loading movies…</p>;

  return (
    <div className="movie-list">
      {movies.map(movie => (
        <div
          key={movie.id}
          className="movie-card movie-link"
          onClick={() => navigate(`/movies/${movie.id}`)}
        >
          <div className="movie-poster-container">
            <img
              className="movie-poster"
              src={movie.poster || '/placeholder.jpg'}
              alt={`${movie.title} poster`}
            />
          </div>
          <div className="movie-details">
            <h2 className="movie-title">{movie.title}</h2>
            <p className="movie-date">{movie.release_date}</p>
            <p className="movie-rating">
              Rating: {movie.rating ? `${movie.rating}/10` : 'TBD'}
            </p>
            <p className="movie-description">{movie.description}</p>

            {movie.trailer
              ? (
                <a
                  className="movie-trailer"
                  href={movie.trailer}
                  target="_blank"
                  rel="noreferrer"
                  onClick={e => e.stopPropagation()}
                >
                  ▶ Watch Trailer
                </a>
              )
              : <span className="no-trailer">No Trailer Available</span>
            }
          </div>
        </div>
      ))}
    </div>
  );
}

export default MovieList;