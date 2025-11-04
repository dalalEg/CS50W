import React, { useEffect, useState, useCallback } from 'react';
import { fetchMovies, searchMovies } from '../api/movies';
import { fetchGenres } from '../api/genre.js';
import { useNavigate } from 'react-router-dom';
import '../styles/MovieList.css';

function MovieList() {
  const [movies, setMovies] = useState([]);
  const [query, setQuery] = useState('');
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const [selectedRating, setSelectedRating] = useState(0);
  const [sortBy, setSortBy] = useState('alpha.desc');
  const [selectedDuration, setSelectedDuration] = useState(180);
  const [selectedYear, setSelectedYear] = useState(2000);
  const [currentPage, setCurrentPage] = useState(1);  // Track current page
  const [hasMorePages, setHasMorePages] = useState(true);  // Track if more pages exist

  // Fetch genres once
  useEffect(() => {
    fetchGenres()
      .then(res => setGenres(res.data))
      .catch(() => {});
  }, []);

  // Fetch movies for the current page (incremental)
  const fetchMoviesData = useCallback(async (page = 1, append = false) => {
    setLoading(true);
    setError(null);
    try {
      const res = query ? await searchMovies(query, page) : await fetchMovies(page);
      const newMovies = res.data.results || res.data;
      if (append) {
        setMovies(prev => [...prev, ...newMovies]);  // Append new movies
      } else {
        setMovies(newMovies);
      }
      setHasMorePages(!!res.data.next);  // Check if more pages exist
    } catch {
      setError('Could not load movies.');
    } finally {
      setLoading(false);
    }
  }, [query]);

  // Load more movies (next page)
  const loadMore = () => {
    const nextPage = currentPage + 1;
    setCurrentPage(nextPage);
    fetchMoviesData(nextPage, true);  // Append mode
  };

  // Fetch on mount or when query/filters change (reset to page 1)
  useEffect(() => {
    setCurrentPage(1);  // Reset page
    fetchMoviesData(1, false);  // Fetch first page
  }, [query, selectedGenre, selectedRating, selectedDuration, selectedYear, sortBy, fetchMoviesData]);

  // Parse duration helper
  const parseDuration = (duration) => {
    if (!duration) return 0;
    const [hours, minutes] = duration.split(':').map(Number);
    return (hours * 60) + minutes;
  };

  // Filter and sort movies client-side (applied to all loaded movies)
  const displayedMovies = movies
    .filter(m => {
      const releaseYear = new Date(m.release_date).getFullYear();
      return (
        (!selectedGenre || m.genres.some(g => g.id === +selectedGenre)) &&
        (m.rating >= selectedRating || m.rating === 0.0) &&
        parseDuration(m.duration) <= selectedDuration &&
        releaseYear >= selectedYear
      );
    })
    .sort((a, b) => {
      if (sortBy === 'popularity.desc') return b.rating - a.rating;
      if (sortBy === 'popularity.asc') return a.rating - b.rating;
      if (sortBy === 'release_date.desc') return new Date(b.release_date) - new Date(a.release_date);
      if (sortBy === 'release_date.asc') return new Date(a.release_date) - new Date(b.release_date);
      if (sortBy === 'alpha.desc') return a.title.localeCompare(b.title);
      if (sortBy === 'alpha.asc') return b.title.localeCompare(a.title);
      if (sortBy === 'duration.desc') return parseDuration(b.duration) - parseDuration(a.duration);
      if (sortBy === 'duration.asc') return parseDuration(a.duration) - parseDuration(b.duration);
      return 0;
    });

  return (
    <div className="movie-list-container">
      <div className="filters">
        <p><strong>Find your perfect movie</strong></p>

        {/* Search Bar */}
        <input
          type="text"
          placeholder="Search by title or keyword..."
          value={query}
          onChange={e => setQuery(e.target.value)}
        />

        {/* Genre */}
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

        {/* Rating */}
        <label>
          Min Rating: {selectedRating.toFixed(1)}
          <input
            className="Rating-selector"
            type="range"
            min="0"
            max="10"
            step="0.1"
            value={selectedRating}
            onChange={e => setSelectedRating(parseFloat(e.target.value))}
          />
        </label>

        {/* Duration */}
        <label>
          Max Duration (minutes):
          <input
            type="number"
            min="0"
            value={selectedDuration}
            onChange={e => setSelectedDuration(Number(e.target.value))}
          />
        </label>

        {/* Release Year */}
        <label>
          Release Year (min):
          <input
            type="number"
            min="1900"
            max={new Date().getFullYear()}
            value={selectedYear}
            onChange={e => setSelectedYear(Number(e.target.value))}
          />
        </label>

        {/* Sort */}
        <label className="sort-label">
          Sort by:
          <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
            <option value="alpha.desc">Alphabetical (A-Z)</option>
            <option value="alpha.asc">Alphabetical (Z-A)</option>
            <option value="popularity.desc">Popularity (High to Low)</option>
            <option value="popularity.asc">Popularity (Low to High)</option>
            <option value="release_date.desc">Release Date (Newest First)</option>
            <option value="release_date.asc">Release Date (Oldest First)</option>
            <option value="duration.desc">Duration (Longest First)</option>
            <option value="duration.asc">Duration (Shortest First)</option>
          </select>
        </label>
      </div>

      {loading && <p>Loading movies...</p>}
      {error && <p>{error}</p>}
      {!loading && !error && displayedMovies.length === 0 && (
        <p>No movies found{query ? ` for “${query}”` : ''}.</p>
      )}

      {/* Movie List */}
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
                IMDb RATING: {movie.rating ? `${movie.rating}/10` : 'TBD'}
              </p>
              <p className="movie-description">{movie.description}</p>
              <p className="movie-duration">Duration: {movie.duration || 'TBD'}</p>
              {movie.trailer ? (
                <a
                  className="movie-trailer"
                  href={movie.trailer}
                  target="_blank"
                  rel="noreferrer"
                  onClick={e => e.stopPropagation()}
                >
                  ▶ Watch Trailer
                </a>
              ) : (
                <span className="no-trailer">No Trailer Available</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Load More Button */}
      {hasMorePages && !loading && (
        <button className="load-more-btn" onClick={loadMore}>
          Load More Movies
        </button>
      )}
      {loading && <p>Loading more...</p>}
    </div>
  );
}

export default MovieList;