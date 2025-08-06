import React, { use, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchShowtimes }   from '../api/showtimes';
import { fetchTheaterById } from '../api/theater';
import './ShowtimeList.css';

function ShowtimeList() {
  const [showtimes, setShowtimes] = useState([]);
  const [theater, setTheater] = useState(null);
  const params = useParams();
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchShowtimes()
      .then(resp => setShowtimes(resp.data))
      .catch(() => setError("Failed to load showtimes"));
  }, []);

  if (error)   return <p className="error">{error}</p>;
  if (!showtimes) return <p className="loading">Loading…</p>;

  return (
    <div className="showtime-list">
      <h1 className="showtime-list-title">Available Showtimes</h1>
      <ul>
        {/* Use map to render each showtime */}
        {showtimes.length === 0 ? (
          <p>No showtimes available</p>
        ) : null}
        {showtimes.map(st => (
          <li key={st.id}>
            <p><strong>Movie:</strong> {st.movie?.title || 'Unknown Movie'}</p>
            <p><strong>Start Time:</strong> {new Date(st.start_time).toLocaleString()}</p>
            <p><strong>Auditorium:</strong> {st.auditorium?.name || 'Unknown auditorium'}</p>
            <p><strong>Theater:</strong> {st.auditorium?.theater?.name || 'Unknown theater'}</p>
            <p><strong>Available Seats:</strong> {st.auditorium?.available_seats??0} seats available</p>
            <p><strong>Click To More Details:</strong></p>
            <Link to={`/showtimes/${st.id}`} className="showtime-link">
              View Details
            </Link>
            <br />
           

          </li>
        ))}
      </ul>
    </div>
  );
}

export default ShowtimeList;

       