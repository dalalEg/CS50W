import React, { useState, useEffect } from "react";
import { useNotifications } from '../contexts/NotificationContext';
import { useAuth } from '../contexts/AuthContext';
import { fetchWatchlistByUser, removeFromWatchlist } from "../api/watchlist";
import { Link } from "react-router-dom";
import '../styles/UserWatchlist.css';

const UserWatchlist = () => {
  const [watchlist, setWatchlist] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const { reload: reloadNotifs } = useNotifications();
  const { user } = useAuth();
  const pageSize = 10;  // Adjust as needed

  useEffect(() => {
    if (!user) return;
    fetchWatchlist(user.id, currentPage);
  }, [user, currentPage]);

  const fetchWatchlist = async (userId, page) => {
    setLoading(true);
    try {
      const response = await fetchWatchlistByUser(userId, page, pageSize);
      const list = Array.isArray(response.data) ? response.data : response.data.results || [];
      setWatchlist(list);
      setTotalPages(Math.ceil((response.data.count || 0) / pageSize));
      setError(null);
    } catch {
      setError("Failed to load user watchlist");
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  if (loading) return <p>Loading user watchlist...</p>;
  if (error) return <p className="text-danger">{error}</p>;
  if (!Array.isArray(watchlist)) return <p>Unexpected data format</p>;

  return (
    <div className="card user-watchlist">
      <h2>Watchlist for {user.username}</h2>
      <ul>
        {watchlist.length === 0 && <p>No movies in watchlist.</p>}
        {watchlist.map(item => (
          <li key={item.id}>
            <Link to={`/movies/${item.movie.id}`}>
              <strong>Movie:</strong> {item.movie.title}
            </Link>
            <button
              onClick={() =>
                removeFromWatchlist(item.id)
                  .then(() => {
                    setWatchlist(prev => prev.filter(w => w.id !== item.id));
                    reloadNotifs();
                  })
                  .catch(() => alert("Failed to remove"))
              }
            >
              Remove
            </button>
          </li>
        ))}
      </ul>
      {/* Pagination Controls */}
      <div className="pagination">
        <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
          Previous
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
};

export default UserWatchlist;
