import React, { use, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchShowtimesByTheater } from '../api/showtimes';
import { fetchTheaterById } from '../api/theater';
import '../styles/TheaterDetails.css';
// TheaterDetails component to display showtimes for a specific theater
function TheaterDetails() {
    const { theaterId } = useParams();
    const [showtimes, setShowtimes] = useState([]);
    const [error, setError] = useState(null);
    const [theater, setTheater] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetchTheaterById(theaterId)
        .then(resp => {
            setTheater(resp.data);
            return fetchShowtimesByTheater(theaterId);
        })
        .then(resp => {
            setShowtimes(resp.data);
            setLoading(false);
        })
        .catch(() => {
            setError("Failed to load showtimes for this theater");
            setLoading(false);
        });
    }, [theaterId]);
    
    if (loading) return <p className="loading">Loading theater details...</p>;
    if (error) return <p className="error">{error}</p>;
    if (!theater) return <p className="error">Theater not found</p>;

    return (
        <div className="theater-details">
            <h1>{theater.name}</h1>
            <p><strong>Location:</strong> {theater.location}</p>
            <h2>Showtimes</h2>
            <ul>
                {showtimes.map(st => (
                    <li key={st.id}>
                        <Link to={`/showtimes/${st.id}`}>{st.movie.title}</Link> - {new Date(st.start_time).toLocaleString()}
                        <p><strong>Auditorium:</strong> {st.auditorium.name}</p>
                        <p><strong>Available Seats:</strong> {st.available_seats}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default TheaterDetails;
