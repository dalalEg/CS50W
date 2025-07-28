import React from 'react';
import MovieList from '../components/MovieList';
import './Home.css';

const Home = () => {
    return (
        <div className="home">
            <h1>Welcome to the Movie Theater Booking App</h1>
            <p>Browse our selection of movies and book your tickets today!</p>
            <MovieList />
        </div>
    );
};

export default Home;