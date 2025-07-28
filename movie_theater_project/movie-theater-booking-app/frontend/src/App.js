import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Booking from './pages/Booking';
import Admin from './pages/Admin';
import MovieList from './components/MovieList';
import SeatSelection from './components/SeatSelection';
import AdminPanel from './components/AdminPanel';
import ReviewSection from './components/ReviewSection';
import './styles/main.css';

function App() {
    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route path="/" exact component={Home} />
                    <Route path="/booking" component={Booking} />
                    <Route path="/admin" component={Admin} />
                    <Route path="/movies" component={MovieList} />
                    <Route path="/seats" component={SeatSelection} />
                    <Route path="/admin-panel" component={AdminPanel} />
                    <Route path="/reviews" component={ReviewSection} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;