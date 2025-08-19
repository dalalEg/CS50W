import React, {useState, useEffect} from "react";
import { useNotifications } from '../contexts/NotificationContext';
import { useAuth }          from '../contexts/AuthContext';
import { fetchWatchlistByUser, removeFromWatchlist } from "../api/watchlist";
import { Link } from "react-router-dom";
import '../styles/UserWatchlist.css';

const UserWatchlist = () => {
  const [watchlist, setWatchlist] = useState([]);
  const [error, setError]         = useState(null);
  const [loading, setLoading]     = useState(true);
  const { reload: reloadNotifs }  = useNotifications();
  const { user }                  = useAuth();

  useEffect(() => {
    if (!user) return;
    fetchWatchlistByUser(user.id)
      .then(resp => {
        // resp.data might be array or wrapped in { results: [...] }
        const list = Array.isArray(resp.data)
          ? resp.data
          : resp.data.results || [];
        setWatchlist(list);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load user watchlist");
        setLoading(false);
      });
  }, [user]);

  if (loading) return <p>Loading user watchlist...</p>;
  if (error)   return <p className="text-danger">{error}</p>;
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
    </div>
  );
};

export default UserWatchlist;
