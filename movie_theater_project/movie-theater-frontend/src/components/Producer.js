import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link, useParams } from 'react-router-dom';
import { fetchProducerById } from '../api/producer';
import { fetchMovieByProducer } from '../api/movies';
import '../styles/Producer.css';
export default function ProducerDetails() {
    const { producerId } = useParams();
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [producer, setProducer] = useState(null);
    const [loading, setLoading] = useState(true);
    const [movies, setMovies] = useState([]);
    useEffect(() => {
        if (!producerId) { setLoading(false); return; }
        (async () => {
            try {
                const resp = await fetchProducerById(producerId);
                setProducer(resp.data);
            } catch (err) {
                setError('Error fetching producer details.');
            } finally {
                setLoading(false);
            }
        })();
    }, [producerId]);

    useEffect(() => {
        if (producerId) {
            fetchMovieByProducer(producerId)
                .then(resp => {
                    setMovies(resp.data);
                })
                .catch(() => setError('Error fetching producer movies.'));
        }
    }, [producerId]);

    if (error) return <div className="text-danger">{error}</div>;
    if (loading) return <div>Loading…</div>;
    if (!producer) return <div>No producer found.</div>;
    return (
        <div className="producer-details">
            <h2>{producer.name} Producer Details</h2>
            {producer && (
                <div>
                    <p><strong>Name:</strong> {producer.name}</p>
                    <p><strong>Bio:</strong> {producer.biography}</p>
                    <p><strong>Birthdate:</strong> {producer.date_of_birth}</p>
                    <p><strong>Movies:</strong></p>
                    <ul>
                        {movies.map(movie => (
                            <li key={movie.id}>
                                <Link to={`/movies/${movie.id}`} className='producer-movie'>{movie.title}</Link>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}