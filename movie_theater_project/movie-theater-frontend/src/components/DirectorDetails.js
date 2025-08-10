import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link, useParams } from 'react-router-dom';
import { fetchDirectorById } from '../api/director';
import { fetchMovieByDirector } from '../api/movies';

export default function DirectorDetails() {
    const { directorId } = useParams();
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [director, setDirector] = useState(null);
    const [loading, setLoading] = useState(true);
    const [movies, setMovies] = useState([]);
    useEffect(() => {
        if (!directorId) { setLoading(false); return; }
        (async () => {
            try {
                const resp = await fetchDirectorById(directorId);
                setDirector(resp.data);
            } catch (err) {
                setError('Error fetching director details.');
            } finally {
                setLoading(false);
            }
        })();
    }, [directorId]);

    useEffect(() => {
        if (directorId) {
            fetchMovieByDirector(directorId)
                .then(resp => {
                    setMovies(resp.data);
                })
                .catch(() => setError('Error fetching director movies.'));
        }
    }, [directorId]);

    if (error) return <div className="text-danger">{error}</div>;
    if (loading) return <div>Loading…</div>;
    if (!director) return <div>No director found.</div>;
    return (
        <div className="director-details">
            <h2>{director.name} Director Details</h2>
            {director && (
                <div>
                    <p><strong>Name:</strong> {director.name}</p>
                    <p><strong>Bio:</strong> {director.biography}</p>
                    <p><strong>Birthdate:</strong> {director.date_of_birth}</p>
                    <p><strong>Movies:</strong></p>
                    <ul>
                        {movies.map(movie => (
                            <li key={movie.id}>
                                <Link to={`/movies/${movie.id}`}>{movie.title}</Link>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}