import React, { use, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchShowtimes ,searchShowtimes }   from '../api/showtimes';
import { fetchGenres } from '../api/genre';
import '../styles/ShowtimeList.css';
import { searchMovies } from '../api/movies';

function ShowtimeList() {
  const [showtimes, setShowtimes] = useState([]);
  const [error, setError] = useState(null);
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState('');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [availableSeats, setAvailableSeats] = useState(1);
  const [language, setLanguage] = useState('');
  const [selectedDate,   setSelectedDate]   = useState('');
  const [timeRange,      setTimeRange]      = useState({ from:'', to:'' });
  const [filterVIP,      setFilterVIP]      = useState(false);
  const [filter3D,       setFilter3D]       = useState(false);
  const [filterParking,  setFilterParking]  = useState(false);
  const [location,       setLocation]       = useState('');
  const [sortBy, setSortBy]   = useState('alpha.desc');
  
  useEffect(() => {
    fetchGenres()
      .then(resp => setGenres(resp.data))
      .catch(() => setError("Failed to load genres"));
  }, []);

   useEffect(() => {
     const load = async () => {
       setLoading(true);
       setError(null);
       try {
         const res = query
           ? await searchShowtimes(query)
           : await fetchShowtimes();
         setShowtimes(res.data);
       } catch {
         setError('Could not load showtimes.');
       } finally {
         setLoading(false);
       }
     };
     load();
   }, [query]);

  if (error)   return <p className="error">{error}</p>;
  if (!showtimes) return <p className="loading">Loading…</p>;
  function parseDuration(durStr='') {
    const [h=0, m=0, s=0] = durStr.split(':').map(n => parseInt(n,10));
    return h*3600 + m*60 + s;
  }

 const displayShowtimes = showtimes
  .filter(st => {
    const start = new Date(st.start_time);
    if (selectedDate && start.toISOString().slice(0,10) !== selectedDate) return false;
    if (timeRange.from && start.getHours() < +timeRange.from) return false;
    if (timeRange.to   && start.getHours() > +timeRange.to)   return false;
    if (language    && st.language.toLowerCase() !== language.toLowerCase()) return false;
    if (filterVIP   && !st.is_VIP)       return false;
    if (filter3D    && !st.thD_available) return false;
    if (filterParking && !st.parking_available) return false;
    if (location    && !st.auditorium?.theater?.location.toLowerCase().includes(location.toLowerCase())) return false;
    if (selectedGenre && !st.movie.genres.some(g=>g.id===+selectedGenre)) return false;
    if (st.available_seats < availableSeats) return false;
    return true;
  })
  .sort((a,b) =>{
    if (sortBy === 'showtime_date.desc') return new Date(b.start_time) - new Date(a.start_time);
    if (sortBy === 'showtime_date.asc') return new Date(a.start_time) - new Date(b.start_time);
    if(sortBy === 'duration.desc') return parseDuration(b.movie?.duration) - parseDuration(a.movie?.duration);
    if (sortBy === 'duration.asc') return parseDuration(a.movie?.duration) - parseDuration(b.movie?.duration);
    return 0;
  });  // soonest first

  return (
    <div className="showtime-list">
      <div className='showtime-list-filter'>
        <p><strong>Find your perfect showtime</strong></p>
        <input 
           type="text"
           placeholder="Search by title or keyword..."
           value={query}
           onChange={e => setQuery(e.target.value)}
        />
        <label>
          Remaining Seats:
          <input
            type="number"
            min="1"
            value={availableSeats}
            onChange={e => setAvailableSeats(e.target.value)}
          />
        </label>
        <select
          className="Genre-selector"
          value={selectedGenre}
          onChange={e => setSelectedGenre(e.target.value)}
        >
          <option value="">All Genres</option>
           {genres.map(g => (
             <option key={g.id} value={g.id}>{g.name}</option>
          ))}
        </select>
        <label>Date:
          <input type="date" value={selectedDate}
             onChange={e=>setSelectedDate(e.target.value)} />
        </label>
        <label>From Hour:
          <input type="number" min="0" max="23"
            value={timeRange.from}
            onChange={e=>setTimeRange(tr=>({...tr,from:e.target.value}))}/>
        </label>
        <label>To Hour:
          <input type="number" min="0" max="23"
            value={timeRange.to}
            onChange={e=>setTimeRange(tr=>({...tr,to:e.target.value}))}/>
        </label>

        <select value={language} onChange={e=>setLanguage(e.target.value)}>
          <option value="">All Languages</option>
          <option>English</option>
          <option>Arabic</option>
          <option>Korean</option>
          <option>Hebrew</option>
          <option>French</option>
        </select>
        <label>
          <input type="checkbox" checked={filterVIP}
                  onChange={_=>setFilterVIP(f=>!f)} /> VIP
        </label>
        <label>
          <input type="checkbox" checked={filter3D}
                  onChange={_=>setFilter3D(f=>!f)} /> 3D
        </label>
        <label>
          <input type="checkbox" checked={filterParking}
                  onChange={_=>setFilterParking(f=>!f)} /> Parking
        </label>
        <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
          <option value="showtime_date.desc">Showtime Date (Closest First)</option>
          <option value="showtime_date.asc">Showtime Date (Farthest First)</option>
          <option value="duration.desc">Duration (Longest First)</option>
          <option value="duration.asc">Duration (Shortest First)</option>
        </select>
      </div>
      <h1 className="showtime-list-title">Available Showtimes ({displayShowtimes.length})</h1>
      <ul className='showtime-container'>
        {displayShowtimes.length === 0 ? (
          <p>No showtimes available</p>
        ) : null}
        {displayShowtimes.map(st => (
          <li key={st.id}>
            <p><strong>Movie:</strong> {st.movie?.title || 'Unknown Movie'}</p>
            <p><strong>Start Time:</strong> {new Date(st.start_time).toLocaleString()}</p>
            <p><strong>Duration:</strong> {st.movie?.duration || 'Unknown Duration'}</p>
            <p><strong>Auditorium:</strong> {st.auditorium?.name || 'Unknown auditorium'}</p>
            <p><strong>Theater:</strong> {st.auditorium?.theater?.name || 'Unknown theater'}</p>
            <p><strong>Available Seats:</strong> {st.available_seats??0} seats available</p>
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

       