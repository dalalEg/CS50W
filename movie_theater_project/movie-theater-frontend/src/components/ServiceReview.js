import React, { useState, useEffect } from 'react';
import { useParams, useNavigate }    from 'react-router-dom';
import { useNotifications }           from '../contexts/NotificationContext';
import {
  createFavorite,
  deleteFavorite,
  fetchFavoritesByMovie
} from '../api/favourite';
// ← make sure this matches your API file!
import { fetchBookingDetails }     from '../api/booking';

import {
  fetchServiceReviews,
  createServiceReview
} from '../api/serviceReview';
import { useAuth } from '../contexts/AuthContext';
import '../styles/ServiceReview.css';
export default function ServiceReview() {
  const { bookingId }           = useParams();
  const navigate                = useNavigate();
  const { user, loading: authLoading } = useAuth();          // grab loading
  const { reload: reloadNotifs} = useNotifications();

  const [movieId, setMovieId]         = useState(null);
  const [reviews, setReviews]         = useState([]);
  const [form, setForm]               = useState({ all_rating:5, show_rating:5, auditorium_rating:5, comment:'' });
  const [error, setError]             = useState(null);
  const [favoriteEntry, setFavoriteEntry] = useState(null);

  // 1) load reviews
  useEffect(() => {
    if (!bookingId) return;
    fetchServiceReviews(bookingId)
      .then(r => setReviews(r.data))
      .catch(() => setError('Failed to load service reviews.'));
  }, [bookingId]);

  // 2) load booking → only after auth and bookingId exist
  useEffect(() => {
    if (authLoading || !user || !bookingId) return;         // ← guard!
    fetchBookingDetails(bookingId)                                  // ← use correct helper
      .then(res => {
        
        setMovieId(res.data.showtime.movie.id);
      })
      .catch(err => {
      });
  }, [authLoading, user, bookingId, navigate]);

  // 3) once we know movieId, see if there's already a favorite
  useEffect(() => {
    if (!movieId || !user) return;
    fetchFavoritesByMovie(movieId)
      .then(r => {
        const favs = Array.isArray(r.data) ? r.data : r.data.results || [];
        setFavoriteEntry(favs[0] || null);
      })
      .catch(() => {
        /* ignore or console.warn */
      });
  }, [movieId, user]);

  const handleToggleFavorite = async () => {
    setError(null);
    try {
      if (!movieId) throw new Error("No movieId");
      if (favoriteEntry) {
        // remove existing
        await deleteFavorite(favoriteEntry.id);
        setFavoriteEntry(null);
      } else {
        // create new
        const res = await createFavorite(movieId);
        setFavoriteEntry(res.data);
      }
      reloadNotifs();
    } catch (err) {
      console.error(err.response?.data || err);
      setError('Failed to update favorites.');
    }
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    try {
      await createServiceReview(bookingId, form);
      const res = await fetchServiceReviews(bookingId);
      setReviews(res.data);
      reloadNotifs();
    } catch (err) {
      setError(
        err.response?.data?.non_field_errors?.[0]
        || 'Could not submit service review.'
      );
    }
  };

  // early return while we’re still logging in
  if (authLoading) {
    return <p>Loading your session…</p>;
  }

  return (
    <div className="service-review">
      <h3>Service Review</h3>
      {error && <p className="error">{error}</p>}

     {user && movieId ? (
        <button  className="submit"  onClick={handleToggleFavorite}>
          {favoriteEntry ? 'Remove from Favorites' : 'Add to Favorites'}
        </button>
      ) : user ? (
        <button disabled>Loading booking…</button>
      ) : null}

      {reviews.length > 0 ? (
        <div className="existing-review">
          <p><strong>You already submitted a review:</strong></p>
          <ul>
            <li>Overall: {reviews[0].all_rating}/5</li>
            <li>Show Quality: {reviews[0].show_rating}/5</li>
            <li>Auditorium: {reviews[0].auditorium_rating}/5</li>
          </ul>
          <p>{reviews[0].comment}</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
           {['all_rating','show_rating','auditorium_rating'].map(key => (
             <div key={key}>
               <label>
                 {key.replace('_',' ').toUpperCase()}: {form[key]}
               </label>
               <input
               className='form-range'
                 type="range"
                 min="1"
                 max="5"
                 value={form[key]}
                 onChange={e => setForm(f => ({
                   ...f, [key]: parseInt(e.target.value,10)
                 }))}
               />
             </div>
           ))}
           <div>
             <label>Comment</label>
             <textarea
               value={form.comment}
               onChange={e => setForm(f => ({ ...f, comment: e.target.value }))}
             />
           </div>
           <button className="submit" type="submit">Submit Review</button>
         </form>
       )}
     </div>
   );
 }