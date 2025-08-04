import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchMovie } from '../api/movies';
import './MovieDetail.css';

function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMovie(id)
      .then(resp => setMovie(resp.data))
      .catch(() => setError("Failed to load movie details"));
  }, [id]);

  if (error) return <p className="error">{error}</p>;
  if (!movie) return <p className="loading">Loading…</p>;

  return (
    <div className="movie-detail">
      <Link to="/">← Back to List</Link>
      <h1>{movie.title}</h1>
      <img
        className="detail-poster"
        src={movie.poster || '/placeholder.jpg'}
        alt={`${movie.title} poster`}
      />
      <div className="info">
        <p><strong>Release Date:</strong> {movie.release_date}</p>
        <p><strong>Rating:</strong> {movie.rating}/10</p>
        <p>{movie.description}</p>
        {movie.trailer &&
          <p>
            <a className="trailer-link" href={movie.trailer} target="_blank" rel="noreferrer">
              ▶ Watch Trailer
            </a>
          </p>
        }
        <p><strong>Genres:</strong> {movie.genre_list}</p>
        <p><strong>Director:</strong> {movie.director.name}</p>
        <p><strong>Actors:</strong> {movie.actors.map(actor => actor.name).join(', ')}</p>
        <p><strong>Created At:</strong> {new Date(movie.created_at).toLocaleDateString()}</p>
        </div>
    </div>
  );
}

export default MovieDetail;
