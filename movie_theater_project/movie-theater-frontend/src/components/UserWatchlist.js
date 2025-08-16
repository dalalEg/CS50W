import React, {useState, useEffect} from "react";
import {useParams, Link} from "react-router-dom";
import {fetchUsers} from '../api/user';
import { fetchWatchlistByUser ,removeFromWatchlist} from "../api/watchlist";
import '../styles/UserWatchlist.css';
const   UserWatchlist = () => {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [watchlist, setWatchlist] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
   
  useEffect(() => {
    fetchUsers(userId)
      .then(resp => {
        setUser(resp.data);
        return fetchWatchlistByUser(userId);
      })
      .then(resp => {
        setWatchlist(resp.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load user watchlist");
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <p>Loading user watchlist...</p>;
  if (error) return <p>{error}</p>;
  if (!user) return <p>User not found</p>;
  

  return (
    <div className="user-watchlist">

        <h2>Watchlist for {user.username}</h2>
        <ul>
            {watchlist.length === 0 && <p>No movies in watchlist.</p>}
            {watchlist.map(item => (
               <li key={item.id}>
                 <Link to={`/movies/${item.movie.id}`}>
                   <p><strong> Movie:</strong></p>{item?.movie?.title ? item.movie.title : 'Unknown Title'}
                 </Link>
                 <button onClick={() => removeFromWatchlist(item.id)
                     .then(() => setWatchlist(wl => wl.filter(w=>w.id!==item.id)))
                     .catch(()=>alert('Failed to remove'))}
                 >Click To remove it from watchlist</button>
               </li>
            ))}
        </ul>

    </div>
  );
};

export default UserWatchlist;
