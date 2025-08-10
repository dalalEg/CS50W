import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchReviewsByMovie, createReview } from '../api/review';

export default function Review() {
  const { id: movieId } = useParams();
  const [reviews, setReviews] = useState([]);
  const [content, setContent] = useState('');
  const [rating, setRating] = useState(5);
  const [error, setError]     = useState(null);

  useEffect(() => {
    fetchReviewsByMovie(movieId)
      .then(resp => setReviews(resp.data))
      .catch(() => setError('Failed to load reviews.'));
  }, [movieId]);

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    try {
      await createReview(movieId, { content, rating });
      setContent('');
      setRating(5);
      const resp = await fetchReviewsByMovie(movieId);
      setReviews(resp.data);
    } catch (err) {
      const data = err.response?.data || {};
      const messages = [];
      if (data.content) messages.push(...data.content);
      if (data.rating)  messages.push(...data.rating);
      setError(messages.join(' ') || 'Failed to submit review.');
    }
  };

  return (
    <div>
      <h3>Reviews</h3>
      {reviews.length === 0 && <p>No reviews yet.</p>}
      <ul>
        {reviews.map(r => (
          <li key={r.id}>
            <strong>{r.user.username}</strong> rated {r.rating}/5
            <p>{r.content}</p>
          </li>
        ))}
      </ul>

      <h4>Write a Review</h4>
      {error && <p className="text-danger">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Rating</label>
          <select
            className="form-control"
            value={rating}
            onChange={e => setRating(+e.target.value)}
          >
            {[1,2,3,4,5].map(n => (
              <option key={n} value={n}>{n}</option>
            ))}
          </select>
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
        <button type="submit" className="btn btn-primary">
          Submit Review
        </button>
      </form>
    </div>
  );
}