import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchMovieById }   from '../api/movies';
import { fetchShowtimesByMovie } from '../api/showtimes';
import { fetchRolesByMovie } from '../api/roles';
import { fetchRole } from '../api/roles';
import '../styles/MovieDetail.css';

function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [error, setError] = useState(null);
  const [showtimes, setShowtimes] = useState([]);
  const [roles, setRoles] = useState([]);
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
  useEffect(() => {
    {
      fetchRolesByMovie(id)
        .then(resp => setRoles(resp.data))
        .catch(() => setError("Failed to load roles"));
    }
  }, [id]);
 
  // If there's an error, display it
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
       <Link to={`/movies/${id}/reviews`} state={{ movieId: id }}>
         <p className="review-link"><strong>Click here to see our clients reviews about {movie.title}</strong></p>
        </Link>
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
        <p><strong>Director:</strong>{' '}
          <Link to={`/directors/${movie.director?.id}`} className="director-link">
            {movie.director?.name}
          </Link>
        </p>
        <p><strong>Producer:</strong>{' '}
          <Link to={`/producers/${movie.producer?.id}`} className="producer-link">
            {movie.producer?.name}
          </Link>
        </p>
        <strong> Main Cast : </strong>
        <ul>
          {roles.length === 0 ? ( 
            <li>No roles available</li>
          ) : (
            roles.map(role => (
              <li key={role.id}>
                <Link to={`/actors/${role.actor?.id}`} className="actor-link">
                  {role.actor?.name}
                </Link>{' '}
                  as {role.character_name}
              </li>
            ))
          )}
        </ul>

       

        <p><strong>Available Showtimes:</strong></p>
        <ul>
          {showtimes.length === 0 ? (
            <li>No showtimes available</li>
          ) : (
            showtimes.map(st => (
              <li key={st.id}>
                {new Date(st.start_time).toLocaleString()} –{' '}
                {st.auditorium?.name || 'Unknown auditorium'} –{' '}
                {st.available_seats} seats available
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
