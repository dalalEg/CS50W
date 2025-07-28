import React, { useState, useEffect } from 'react';
import SeatSelection from '../components/SeatSelection';

const Booking = () => {
    const [showtimes, setShowtimes] = useState([]);
    const [selectedShowtime, setSelectedShowtime] = useState(null);

    useEffect(() => {
        // Fetch showtimes from the backend API
        const fetchShowtimes = async () => {
            try {
                const response = await fetch('/api/showtimes/');
                const data = await response.json();
                setShowtimes(data);
            } catch (error) {
                console.error('Error fetching showtimes:', error);
            }
        };

        fetchShowtimes();
    }, []);

    const handleShowtimeSelect = (showtime) => {
        setSelectedShowtime(showtime);
    };

    return (
        <div className="booking-page">
            <h1>Book Your Tickets</h1>
            <div className="showtime-list">
                {showtimes.map((showtime) => (
                    <div key={showtime.id} className="showtime-item" onClick={() => handleShowtimeSelect(showtime)}>
                        <h2>{showtime.movie.title}</h2>
                        <p>{showtime.time}</p>
                    </div>
                ))}
            </div>
            {selectedShowtime && <SeatSelection showtime={selectedShowtime} />}
        </div>
    );
};

export default Booking;