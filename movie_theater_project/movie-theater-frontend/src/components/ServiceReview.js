import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useNotifications } from '../contexts/NotificationContext';

import {
  fetchServiceReviews,
  createServiceReview
} from '../api/serviceReview';
import '../styles/ServiceReview.css';
 export default function ServiceReview() {
   const { bookingId } = useParams();
   const [reviews, setReviews] = useState([]);
   const [form, setForm]       = useState({
     all_rating: 5,
     show_rating: 5,
     auditorium_rating: 5,
     comment: ''
   });
   const [error, setError]     = useState(null);
   const { reload: reloadNotifs }  = useNotifications();

   useEffect(() => {
    if (!bookingId) return;
     fetchServiceReviews(bookingId)
       .then(res => setReviews(res.data))
       .catch(() => setError('Failed to load service reviews.'));
   }, [bookingId]);

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

   return (
     <div className="service-review">
       <h3>Service Review</h3>
       {error && <p className="error">{error}</p>}

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