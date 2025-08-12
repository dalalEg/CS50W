import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchReviewsByMovie, createReview,makeReviewAnonymous } from '../api/review';
import RatingReview from "./RatingReview" // add you floder path properly
import '../styles/Review.css'
export default function Review() {
  const { id: movieId } = useParams();
  const [reviews, setReviews] = useState([]);
  const [content, setContent] = useState('');
  const [rating, setRating] = useState(5);
  const [error, setError] = useState(null);
  const [anonymous, setAnonymous] = useState(false);
  
  useEffect(() => {
    fetchReviewsByMovie(movieId)
      .then(resp => setReviews(resp.data))
      .catch(() => setError('Failed to load reviews.'));
  }, [movieId]);

   
  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    try {
      await createReview(movieId, { content, rating ,anonymous});
      setContent('');
      setRating(5);
      const resp = await fetchReviewsByMovie(movieId);
      setReviews(resp.data);
    } catch (err) {
      // Handle error messages from the backend
      const status = err.response?.status;
      if (status === 401 || status === 403) {
        setError('You are not authorized to perform this action, please log in.');
        return;
      }
      const data = err.response?.data || {};
      const messages = [];
      if (data.content) messages.push(...data.content);
      if (data.rating)  messages.push(...data.rating);
      setError(messages.join(' ') || 'Failed to submit review.');
    }
  };

  return (
    <div className="review-container">
      <div className='reviews'>
        <h3>Reviews</h3>
        {reviews.length === 0 && <p>No reviews yet.</p>}
        <ul>
          {reviews.map(r => (
            <li key={r.id}>
              <strong>{r.anonymous ? 'Anonymous' : r.user.username}</strong> rated {r.rating}/5
              <p>{r.content}</p>
            </li>
          ))}
        </ul>
      </div>
      <div className='inline'> </div>
      <div className='write-review'>
        <h4>Write a Review</h4>
        {error && <p className="text-danger">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label>Rating: {rating}/5</label>
            <RatingReview rating={rating} setRating={setRating} />

          </div>
          <div className="mb-3">
            <label>Content</label>
            <textarea
              className="form-control"
              value={content}
              onChange={e => setContent(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label>Anonymous</label>
            <input
              type="checkbox"
              checked={anonymous}
              onChange={e => setAnonymous(e.target.checked)}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Submit Review
          </button>
        </form>
      </div>  
    </div>
      
  );
}