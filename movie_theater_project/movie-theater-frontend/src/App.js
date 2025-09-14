import './App.css';
import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import NavBar   from './components/NavBar';
import MovieList   from './components/MovieList';
import MovieDetail from './components/MovieDetail';
import Login       from './components/Login';
import Register    from './components/Register';
import Profile     from './components/Profile';
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
import PrivateRoute from './components/PrivateRoute';
import AdminDashboard from './components/AdminDashboard';
import News from './components/News';
import { useAuth } from './contexts/AuthContext';

// Main App component
function App() {
  const { user, loading, logout } = useAuth();
  const handleLogout = logout;
  // on mount, you might ping /api/auth/user or read a cookie/token
  if (loading) return <p className="loading">Loading…</p>;

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
              <PrivateRoute>
                <Profile/>
              </PrivateRoute>
            }
          />
          <Route path="*"            element={<h2>Page not found</h2>} />
          <Route path="/showtimes" element={<ShowtimeList />} />
          <Route path="/showtimes/:id" element={<ShowtimeDetail />} />
          <Route path="/theaters" element={<TheaterListing />} />
          <Route path="/booking" element={<PrivateRoute><Booking /></PrivateRoute>} />
          <Route path="/bookings/:bookingId" element={<PrivateRoute><BookingDetail /></PrivateRoute>} />
          <Route path="/directors/:directorId" element={<DirectorDetails />} />
          <Route path="/producers/:producerId" element={<ProducerDetails />} />
          <Route path="/theaters/:theaterId" element={<TheaterDetails />} />
          <Route path="/actors/:actorId" element={<ActorDetails />} />
          <Route path="/movies/:id/reviews" element={<Review />} />
          <Route path="/user/bookings/:id" element={<PrivateRoute><UserBooking /></PrivateRoute>} />
          <Route path="/reviews/:userId" element={<PrivateRoute><UserReview /></PrivateRoute>} />
          <Route path="/watchlist/:userId" element={<PrivateRoute><UserWatchlist /></PrivateRoute>} />
          <Route path="/admin/*" element={<AdminPanel />} />
          <Route path="/user/edit/:id" element={<PrivateRoute><EditUser /></PrivateRoute>} />
          <Route path="/serviceReview/:bookingId" element={<PrivateRoute><ServiceReview /></PrivateRoute>} />
          <Route path="/news" element={<News />} />
          <Route path="/notifications" element={<PrivateRoute><NotificationsList /></PrivateRoute>} />
          <Route path="/admin/dashboard" element={<PrivateRoute>{user?.is_staff ? <AdminDashboard /> : <Navigate to="/login" />}</PrivateRoute>} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
