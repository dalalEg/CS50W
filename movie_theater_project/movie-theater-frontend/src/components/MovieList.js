import React, { use, useEffect, useState } from 'react';
import { fetchMovies,searchMovies } from '../api/movies';
import { fetchGenres } from '../api/genre.js';
import { useNavigate }  from 'react-router-dom';
import '../styles/MovieList.css';

function MovieList() {
  const [movies, setMovies] = useState([]);
  const [query, setQuery]   = useState('');
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);
  const navigate              = useNavigate();
  const [selectedRating, setSelectedRating] = useState(0);
  const [sortBy, setSortBy]   = useState('alpha.desc');

  useEffect(() => {
    fetchGenres()
      .then(res => setGenres(res.data))
      .catch(() => {/* ignore */});
  }, []);
  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = query
          ? await searchMovies(query)
          : await fetchMovies();
        setMovies(res.data);
      } catch {
        setError('Could not load movies.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [query]);
    const displayedMovies = movies.filter(m =>
    (!selectedGenre || m.genres.some(g => g.id === +selectedGenre)) &&
    m.rating >= selectedRating
  ).sort((a, b) => {
      if (sortBy === 'popularity.desc') {
        return b.rating - a.rating;
      } else if (sortBy === 'popularity.asc') {
        return a.rating - b.rating;
      } else if (sortBy === 'release_date.desc') {
        return new Date(b.release_date) - new Date(a.release_date);
      } else if (sortBy === 'release_date.asc') {
        return new Date(a.release_date) - new Date(b.release_date);
      } else if (sortBy === 'alpha.desc') {
        return a.title.localeCompare(b.title);
      } else if (sortBy === 'alpha.asc') {
        return b.title.localeCompare(a.title);
      }
      return 0;
  });
  return (
    <div className="movie-list-container">
      <div className="filters">
        <p><strong>Want to search about a specific movie?</strong></p>
        <input
          type="text"
          placeholder="Search by title or keyword..."
          value={query}
          onChange={e => setQuery(e.target.value)}
        />

        <select
          className='Genre-selector'
          value={selectedGenre}
          onChange={e => setSelectedGenre(e.target.value)}
        >
          <option value="">All Genres</option>
          {genres.map(g => (
            <option key={g.id} value={g.id}>{g.name}</option>
          ))}
        </select>

        <label style={{ marginLeft: 16 }}>
          Min Rating: {selectedRating.toFixed(1)}
        </label>
        <input
          className='Rating-selector'
          type="range"
          min="0"
          max="10"
          step="0.1"
          value={selectedRating}
          onChange={e => setSelectedRating(parseFloat(e.target.value))}
        />
        <label className="sort-label">
          Sort by:  <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
            <option value="alpha.desc">Alphabetical (A-Z)</option>
            <option value="alpha.asc">Alphabetical (Z-A)</option>
            <option value="popularity.desc">Popularity (High to Low)</option>
            <option value="popularity.asc">Popularity (Low to High)</option>
            <option value="release_date.desc">Release Date (Newest First)</option>
            <option value="release_date.asc">Release Date (Oldest First)</option>
          </select>
        </label>
        <label className='release-label'>
          Release Date:
        </label>
      </div>
    

      {!loading && !error && displayedMovies.length === 0 && (
        <p>No movies found{query ? ` for “${query}”` : ''}.</p>
      )}
  
    <div className="movie-list">

      {displayedMovies.map(movie => (
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
    </div>
  );
}

export default MovieList;