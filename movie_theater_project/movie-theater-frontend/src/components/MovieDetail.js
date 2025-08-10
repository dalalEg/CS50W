import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchMovieById }   from '../api/movies';
import { fetchShowtimesByMovie } from '../api/showtimes';
import './MovieDetail.css';

function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [error, setError] = useState(null);
  const [showtimes, setShowtimes] = useState([]);

  useEffect(() => {
    fetchMovieById(id)
      .then(resp => setMovie(resp.data))
      .catch(() => setError("Failed to load movie details"));
  }, [id]);
  useEffect(() => {
    {
      fetchShowtimesByMovie(id)
        .then(resp => setShowtimes(resp.data))
        .catch(() => setError("Failed to load showtimes"));
    }
  }, [id]);
  if (error)   return <p className="error">{error}</p>;
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

        {/* Instead of a lone block, use parentheses */}
        {movie.trailer && (
          <p>
            <a
              className="trailer-link"
              href={movie.trailer}
              target="_blank"
              rel="noreferrer"
            >
              ▶ Watch Trailer
            </a>
          </p>
        )}

        <p><strong>Genres:</strong> {movie.genre_list}</p>
        
        <Link to={`/directors/${movie.director?.id}`} className="director-link">
        <p>
          <strong>Director:</strong>{' '}
          {movie.director?.name || 'Unknown'}
        </p>
      </Link>
      <p>
        <strong>Actors:</strong>{' '}
        {movie.actors.map(a => a.name).join(', ')}
      </p>

        <p><strong>Available Showtimes:</strong></p>
        <ul>
          {showtimes.length === 0 ? (
            <li>No showtimes available</li>
          ) : (
            showtimes.map(st => (
              <li key={st.id}>
                {new Date(st.start_time).toLocaleString()} –{' '}
                {st.auditorium?.name || 'Unknown auditorium'} –{' '}
                {st.auditorium.available_seats} seats available
                <Link to={`/showtimes/${st.id}`} className="showtime-link">
                  Click For More Details
                </Link>
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}

export default MovieDetail;
