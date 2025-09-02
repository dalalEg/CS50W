import React, { useEffect, useState } from 'react';  // remove the invalid `use` import
import { useNavigate } from 'react-router-dom';
import { fetchTheaters ,searchTheaters}          from '../api/theater';
import { fetchAuditoriumByTheater } from '../api/auditorium';
import '../styles/TheaterListing.css';

const TheaterListing = () => {
  const navigate = useNavigate();
  const [theaters, setTheaters] = useState([]);
  const [error, setError]       = useState(null);
  const [location, setLocation] = useState('');
  useEffect(() => {
    let isMounted = true;
    fetchTheaters()
      .then(res => {
        const list = res.data;
        // fetch auditoriums in parallel for each theater
        return Promise.all(
          list.map(t =>
            fetchAuditoriumByTheater(t.id)
              .then(r => ({ ...t, auditoriums: r.data }))
          )
        );
      })
      .then(withAuditoriums => {
        if (isMounted) setTheaters(withAuditoriums);
      })
      .catch(err => {
        if (isMounted) setError(err.message);
      });
    return () => { isMounted = false; };
  }, []);  // only run once
  useEffect(() => {
    if (location) {
      const timer = setTimeout(() => {
        searchTheaters(location)
          .then(res => setTheaters(res.data))
          .catch(err => setError(err.message));
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [location]);
  if (error)               return <p className="error">{error}</p>;
  if (!theaters)           return <p className="error">No theaters found</p>;
  return (
    <div className="theater-listing container mt-4">
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search by location..."
          value={location}
          onChange={e => setLocation(e.target.value)}
        />
    </div>
    <div className="theater-listing">
      <h2>Theater Listings</h2>
      <ul>
        {theaters.length === 0 ? (
          <li>No theaters found</li>
        ) : (
          theaters.map(theater => (
            <div key={theater.id} onClick={()=>navigate(`/theaters/${theater.id}`)} className="theater-card">
              <div className="theater-info">
                <h3>{theater.name}</h3>
                <p><strong>Location:</strong> {theater.location}</p>
            <p><strong>Auditoriums:</strong></p>
            <ul>
              {theater.auditoriums?.length > 0 ? (
                theater.auditoriums.map(aud => (
                  <li key={aud.id}> 
                    <p><strong>Auditorium Name:</strong> {aud.name}</p>
                    <p><strong>Capacity:</strong> {aud.total_seats}</p>
                  </li>
                ))
              ) : (
                <li>No auditoriums available</li>
              )}
            </ul>
            </div>
          </div>
        )))}
      </ul>
    </div>
    </div>
  );
};

export default TheaterListing;
