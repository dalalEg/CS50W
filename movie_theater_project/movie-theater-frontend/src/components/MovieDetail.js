import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchMovieById }   from '../api/movies';
import { fetchShowtimesByMovie } from '../api/showtimes';
import { useAuth } from '../contexts/AuthContext';
import { fetchRolesByMovie } from '../api/roles';
import { useNotifications } from '../contexts/NotificationContext';

import { addToWatchlist,fetchWatchlistByUser,removeFromWatchlist } from '../api/watchlist';

import '../styles/MovieDetail.css';

function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [error, setError] = useState(null);
  const [showtimes, setShowtimes] = useState([]);
  const [roles, setRoles] = useState([]);
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const { user: currentUser, loading: authLoading } = useAuth();
  const { reload: reloadNotifs }  = useNotifications();
  const [watchlistEntryId, setWatchlistEntryId] = useState(null);
  useEffect(() => {
    fetchMovieById(id)
      .then(resp => setMovie(resp.data))
      .catch(() => setError("Failed to load movie details"));
  }, [id]);
  useEffect(() => {
    
      fetchShowtimesByMovie(id)
        .then(resp => setShowtimes(resp.data))
        .catch(() => setError("Failed to load showtimes"));
    
  }, [id]);

  useEffect(() => {
    
      fetchRolesByMovie(id)
        .then(resp => setRoles(resp.data))
        .catch(() => setError("Failed to load roles"));
    
  }, [id]);

  useEffect(() => {
    if (!currentUser) return;
    fetchWatchlistByUser(currentUser.id)
      .then(resp => {
       const found = resp.data.find(item => item.movie?.id === parseInt(id, 10));
       setIsInWatchlist(Boolean(found));
       setWatchlistEntryId(found?.id ?? null);
      })
      .catch(() => setError("Failed to load watchlist"));
  }, [currentUser, id]);

  const handleAddOrRemoveFromWatchlist = () => {
    if (isInWatchlist) {
      removeFromWatchlist(watchlistEntryId)
        .then(() => {
          setIsInWatchlist(false);
          setWatchlistEntryId(null);
          reloadNotifs();
        })
        .catch(err => {
          console.error(err);
          setError("Failed to remove from watchlist");
        });
    } else {
      addToWatchlist(id)
        .then(resp => {
          setIsInWatchlist(true);
          setWatchlistEntryId(resp.data.id);
          reloadNotifs();
        })
        .catch(err => {
          const errs = err.response?.data?.non_field_errors || [];
          // if already exists, mark as in-watchlist
          if (errs.some(e => e.includes('already in your watchlist'))) {
            setIsInWatchlist(true);
            return;
          }
          console.error(err.response?.data || err);
          setError("Failed to add to watchlist");
        });
     }
   };
  if (error)   return <p className="error">{error}</p>;
  if (!movie) return <p className="loading">Loading…</p>;
  if (authLoading) return <p className="loading">Loading…</p>;
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
        <p><strong>Duration:</strong> {movie.duration} minutes</p>
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
         <button
                onClick={handleAddOrRemoveFromWatchlist}
                className='watchlist-button'
              >
                {isInWatchlist ? 'Already in Watchlist' : 'Add to Watchlist'}
              </button>
        <ul>
          {showtimes.length === 0 ? (
            <li className='no-showtimes'>No showtimes available you can add this movie to your watchlist:
             
            </li>
           
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
