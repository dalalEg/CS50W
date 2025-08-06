import './App.css';
import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Navigate          // ← import Navigate
} from 'react-router-dom';
import NavBar   from './components/NavBar';
import MovieList   from './components/MovieList';
import MovieDetail from './components/MovieDetail';
import Login       from './components/Login';
import Register    from './components/Register';
import Profile     from './components/Profile';
import { api }     from './api/axios';
import  ShowtimeList from './components/ShowtimeList';
import ShowtimeDetail from './components/ShowtimeDatail';
import TheaterListing from './components/TheaterListing';
// Main App component
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername]               = useState('');

  // on mount, you might ping /api/auth/user or read a cookie/token
  useEffect(() => {
    api.get('/api/auth/user/')
      .then(r => {
        setIsAuthenticated(true);
        setUsername(r.data.username);
      })
      .catch(() => {
        setIsAuthenticated(false);
        setUsername('');
      });
  }, []);
  useEffect(() => {
    if(isAuthenticated){
      // fetch user details if authenticated
      api.get('/api/auth/user/')
        .then(r => setUsername(r.data.username))
        .catch(() => setIsAuthenticated(false));
    }
  }, [isAuthenticated]);
  const handleLogout = () => {
    // in App.js or wherever
    api.post('/api/auth/logout/').finally(() => {
      setIsAuthenticated(false);
      setUsername('');
    });
  };

  return (
    <Router>
      <header className="App-header">
        <h1>🎬 Dali Movie Theater</h1>
      </header>

      {/* now NavBar owns the profile link */}
      <NavBar
        isAuthenticated={isAuthenticated}
        username={username}
        onLogout={handleLogout}
      />
         
      <main className="container mt-4 ">
        <Routes className="Routes">
          <Route path="/"            element={<MovieList />} />
          <Route path="/movies/:id"  element={<MovieDetail />} />
          <Route path="/login"       element={<Login onLogin={() => setIsAuthenticated(true)} />} />
          <Route path="/register"    element={<Register onRegister={() => setIsAuthenticated(true)} />} />
          <Route
            path="/profile"
            element={
              isAuthenticated
                ? <Profile />
                : <Navigate to="/login" replace />    // ← redirect if signed out
            }
          />
          <Route path="*"            element={<h2>Page not found</h2>} />
          <Route path="/showtimes" element={<ShowtimeList />} />
          <Route path="/showtimes/:id" element={<ShowtimeDetail />} />
          <Route path="/theaters" element={<TheaterListing />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
