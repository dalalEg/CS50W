import './App.css';
import React, {useEffect } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Navigate,
  useNavigate
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
import Booking from './components/Booking';
import BookingDetail from './components/BookingDetail';
import DirectorDetails from './components/DirectorDetails'; 
import ProducerDetails from './components/Producer'; 
import TheaterDetails from './components/TheaterDetails'; 
import ActorDetails from './components/Actor'; // Import ActorDetails component
import Review from './components/Review';
import UserBooking from './components/UserBooking'; // Import UserBooking component
import UserReview from './components/UserReview'; // Import UserReview component
import UserWatchlist from  './components/UserWatchlist'; 
import AdminPanel from './AdminPanel';
import EditUser from './components/EditUser'; // Import EditUser component
import ServiceReview from './components/ServiceReview';
import NotificationsList from './components/Notifications';
import { useAuth } from './contexts/AuthContext';

// Main App component
function App() {
  const { user, loading, logout } = useAuth();
  const handleLogout = logout;
  // on mount, you might ping /api/auth/user or read a cookie/token


  return (
    <Router>
      <header className="App-header">
        <h1>🎬 Dali Movie Theater</h1>
      </header>

      {/* now NavBar owns the profile link */}
      <NavBar
        onLogout={handleLogout}
      />
         
      <main className="container mt-4 ">
        <Routes className="Routes">
          <Route path="/"            element={<MovieList />} />
          <Route path="/movies/:id"  element={<MovieDetail />} />
          <Route path="/login"       element={<Login   />}  />
          <Route path="/register"    element={<Register  />} />
          <Route
            path="/profile"
            element={
              loading
                ? <p>Loading…</p>
                : user
                  ? <Profile/>
                  : <Navigate to="/login"/>
            }
          />

          <Route path="*"            element={<h2>Page not found</h2>} />
          <Route path="/showtimes" element={<ShowtimeList />} />
          <Route path="/showtimes/:id" element={<ShowtimeDetail />} />
          <Route path="/theaters" element={<TheaterListing />} />
          <Route path="/booking" element={<Booking />} />
          <Route path="/bookings/:bookingId" element={<BookingDetail />} />
          <Route path="/directors/:directorId" element={<DirectorDetails />} />
          <Route path="/producers/:producerId" element={<ProducerDetails />} />
          <Route path="/theaters/:theaterId" element={<TheaterDetails />} />
          <Route path="/actors/:actorId" element={<ActorDetails />} />
          <Route path="/movies/:id/reviews" element={<Review />} />
          <Route path="/user/bookings/:id" element={<UserBooking />} />
          <Route path="/reviews/:userId" element={<UserReview />} />
          <Route path="/watchlist/:userId" element={<UserWatchlist />} />
          <Route path="/admin/*" element={<AdminPanel />} />
          <Route path="/user/edit/:id" element={<EditUser />} />
          <Route path="/serviceReview/:bookingId" element={<ServiceReview />} />
          <Route path="/notifications" element={<NotificationsList />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
