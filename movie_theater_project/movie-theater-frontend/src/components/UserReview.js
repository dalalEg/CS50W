import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from '../contexts/AuthContext';
import { useNotifications } from '../contexts/NotificationContext';
import RatingReview from "./RatingReview";
import { fetchReviewsByUser, handleDeleteReview, handleUpdateReview } from "../api/review";
import '../styles/UserReview.css';

const UserReview = () => {
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editedReview, setEditedReview] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const { reload: reloadNotifs } = useNotifications();
  const { user } = useAuth();
  const pageSize = 10;  // Adjust as needed

  useEffect(() => {
    if (!user) return;
    fetchReviews(user.id, currentPage);
  }, [user, currentPage]);

  const fetchReviews = async (userId, page) => {
    setLoading(true);
    try {
      const response = await fetchReviewsByUser(userId, page, pageSize);
      setReviews(response.data.results || response.data);
      setTotalPages(Math.ceil((response.data.count || 0) / pageSize));
      setError(null);
    } catch {
      setError("Failed to load user reviews");
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  if (loading) return <p>Loading user reviews...</p>;
  if (error) return <p>{error}</p>;
  if (!user) return <p>User not found</p>;

  const handleDelete = (reviewId) => {
    handleDeleteReview(reviewId)
      .then(() => {
        setReviews(reviews.filter(review => review.id !== reviewId));
        reloadNotifs();
      })
      .catch(() => {
        setError("Failed to delete review");
      });
  };

  const handleEdit = (reviewId) => {
    const review = reviews.find(r => r.id === reviewId);
    if (review) {
      setEditedReview(review);
      setIsEditing(true);
    }
  };

  const handleEditSubmit = (e) => {
    e.preventDefault();
    handleUpdateReview(editedReview.id, editedReview)
      .then(() => {
        setReviews(reviews.map(review => review.id === editedReview.id ? editedReview : review));
        setIsEditing(false);
        setEditedReview(null);
        reloadNotifs();
      })
      .catch(() => {
        setError("Failed to update review");
      });
  };

  return (
    <div className="user-review">
      <h2>Reviews by {user.username}</h2>
      <ul>
        {reviews.length === 0 && <p>No you did not post a review yet.</p>}
        {reviews.map(review => (
          <li key={review.id}>
            <Link to={`/movies/${review?.movie?.id}/reviews`} className="link">
              {review?.movie?.title}
            </Link>
            {isEditing && editedReview?.id === review.id ? (
              <form onSubmit={handleEditSubmit}>
                <h3>Edit Review</h3>
                <label>Rating: {editedReview.rating}/5</label>
                <RatingReview rating={editedReview.rating} setRating={(rating) => setEditedReview({ ...editedReview, rating })} />
                <label>Comment:</label>
                <textarea
                  value={editedReview.content}
                  onChange={(e) => setEditedReview({ ...editedReview, content: e.target.value })}
                />
                <label>
                  <strong>Anonymous:</strong>
                  <input
                    type="checkbox"
                    checked={editedReview.anonymous}
                    onChange={(e) => setEditedReview({ ...editedReview, anonymous: e.target.checked })}
                  />
                </label>
                <button type="submit">Save</button>
                <button type="button" onClick={() => setIsEditing(false)}>Cancel</button>
              </form>
            ) : (
              <>
                <p><strong>Rating:</strong> {review.rating}</p>
                <p><strong>Comment:</strong> {review.content}</p>
                <p><strong>Anonymous:</strong> {review.anonymous ? "Yes" : "No"}</p>
                <p><strong>Created At:</strong> {new Date(review.created_at).toLocaleString()}</p>
                <button onClick={() => handleDelete(review.id)}>Delete Review</button>
                <button onClick={() => handleEdit(review.id)}>Edit Review</button>
              </>
            )}
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

export default UserReview;
