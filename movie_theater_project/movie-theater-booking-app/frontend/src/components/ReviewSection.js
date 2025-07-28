import React, { useState, useEffect } from 'react';

const ReviewSection = ({ movieId }) => {
    const [reviews, setReviews] = useState([]);
    const [newReview, setNewReview] = useState('');
    
    useEffect(() => {
        fetch(`/api/movies/${movieId}/reviews`)
            .then(response => response.json())
            .then(data => setReviews(data))
            .catch(error => console.error('Error fetching reviews:', error));
    }, [movieId]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (newReview.trim()) {
            fetch(`/api/movies/${movieId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ review: newReview }),
            })
            .then(response => response.json())
            .then(data => {
                setReviews([...reviews, data]);
                setNewReview('');
            })
            .catch(error => console.error('Error submitting review:', error));
        }
    };

    return (
        <div className="review-section">
            <h2>Reviews</h2>
            <ul>
                {reviews.map((review, index) => (
                    <li key={index}>{review}</li>
                ))}
            </ul>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={newReview}
                    onChange={(e) => setNewReview(e.target.value)}
                    placeholder="Write your review here..."
                />
                <button type="submit">Submit Review</button>
            </form>
        </div>
    );
};

export default ReviewSection;