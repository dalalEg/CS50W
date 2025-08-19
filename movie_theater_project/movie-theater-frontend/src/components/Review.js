import React, { useState, useEffect, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import { fetchReviewsByMovie, createReview } from '../api/review';
import RatingReview from "./RatingReview";
import { useAuth } from '../contexts/AuthContext';
import { useNotifications } from '../contexts/NotificationContext';

import '../styles/Review.css';

export default function Review() {
  const { id: movieId } = useParams();
  const [reviews, setReviews]     = useState([]);
  const [content, setContent]     = useState('');
  const [rating, setRating]       = useState(5);
  const [anonymous, setAnonymous] = useState(false);
  const [error, setError]         = useState(null);
  const { user } = useAuth();
  const { reload: reloadNotifs } = useNotifications(); 
  // load reviews once
  useEffect(() => {
    fetchReviewsByMovie(movieId)
      .then(resp => setReviews(resp.data))
      .catch(() => setError('Failed to load reviews.'));
  }, [movieId]);

  // derive counts & average on-the-fly whenever reviews change
  const count = reviews.length;
  const anonymousCount = useMemo(
    () => reviews.filter(r => r.anonymous).length,
    [reviews]
  );
  const averageRating = useMemo(() => {
    if (reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, r) => acc + r.rating, 0);
    return sum / reviews.length;
  }, [reviews]);

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    if (!user?.email_verified) {
      setError('Please confirm your email before placing a booking.');
      return;
    }
    try {
      await createReview(movieId, { content, rating, anonymous });
      await reloadNotifs();
      setContent('');
      setRating(5);
      setAnonymous(false);
      // re­fetch and update reviews (which will recalc average automatically)
      const resp = await fetchReviewsByMovie(movieId);
      setReviews(resp.data);
    } catch (err) {
      const status = err.response?.status;
      if (status === 401 || status === 403) {
        setError('You are not authorized, please log in or verify your email address.');
        return;
      }
      const data = err.response?.data || {};
      const msgs = [];
      if (data.content)   msgs.push(...data.content);
      if (data.rating)    msgs.push(...data.rating);
      if (data.anonymous) msgs.push(...data.anonymous);
      setError(msgs.join(' ') || 'Failed to submit review.');
    }
  };

  return (
    <div className="review-container">
      <div className="reviews">
        <h3>Reviews ({count})</h3>
        <p>
          Total: {count} | Anonymous: {anonymousCount} | 
          Average Rating: {averageRating.toFixed(1)}/5
        </p>
        {count === 0 && <p>No reviews yet.</p>}
        <ul>
          {reviews.map(r => (
            <li key={r.id}>
              <strong>{r.anonymous ? 'Anonymous' : r.user.username}</strong> 
              { } rated {r.rating}/5
              <p>{r.content}</p>
            </li>
          ))}
        </ul>
      </div>

      <div className="write-review">
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
            <label>
              <input
                type="checkbox"
                checked={anonymous}
                onChange={e => setAnonymous(e.target.checked)}
              />{' '}
              Post as Anonymous
            </label>
          </div>
          <button type="submit" className="btn btn-primary">
            Submit Review
          </button>
        </form>
      </div>
    </div>
  );
}