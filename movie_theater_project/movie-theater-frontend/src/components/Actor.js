import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link, useParams } from 'react-router-dom';
import { fetchActorById } from '../api/actor';
import { fetchMovieByActor } from '../api/movies';
import '../styles/Actor.css';

export default function ActorDetails() {
    const { actorId } = useParams();
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [actor, setActor] = useState(null);
    const [loading, setLoading] = useState(true);
    const [movies, setMovies] = useState([]);
    useEffect(() => {
        if (!actorId) { setLoading(false); return; }
        (async () => {
            try {
                const resp = await fetchActorById(actorId);
                setActor(resp.data);
            } catch (err) {
                setError('Error fetching actor details.');
            }
            finally {
                setLoading(false);
            }   
        })();
    }, [actorId]);

    useEffect(() => {
        if (actorId) {
            fetchMovieByActor(actorId)
                .then(resp => {
                    setMovies(resp.data);
                })
                .catch(() => setError('Error fetching actor movies.'));
        }
    }, [actorId]);

    if (error) return <div className="text-danger">{error}</div>;
    if (loading) return <div>Loading…</div>;
    if (!actor) return <div>No actor found.</div>;
    return (
        <div className="actor-details">
            <h2>{actor.name} Actor Details</h2>
            {actor && (
                <div>
                    <p><strong>Name:</strong> {actor.name}</p>
                    <p><strong>Biography:</strong> {actor.biography}</p>
                    <p><strong>Date of Birth:</strong> {actor.date_of_birth}</p>
                    <p><strong>Movies:</strong></p>
                    <ul>
                        {movies.map(movie => (
                            <li key={movie.id} >
                                <Link to={`/movies/${movie.id}`} className="actor-movie">{movie.title}</Link>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}