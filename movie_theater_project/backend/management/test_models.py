from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import (User, Movie, Genre,Seat,Showtime,Review, 
                     Notification,Booking,Actor,Director,Auditorium,Producer,Payment,watchlist,Role,Theater)
from django.utils import timezone  # <-- Add this import
from datetime import timedelta
from django.utils.timezone import make_aware, datetime
# Define the User model for testing
# Ensure you have the correct User model imported
User = get_user_model()
class UserModelTest(TestCase):
    """Test case for User model."""
    def setUp(self):
        """Create a user instance for testing."""
        # Create a user instance with username, password, and email
        # You can also set other fields if needed
        self.user = User.objects.create_user(username="dalal", password="test123", email="dalal@example.com")
    def test_user_creation(self):
        """Test that the user is created with the correct attributes."""
        # Check if the user is created with the correct attributes
        self.assertEqual(self.user.username, "dalal")
        self.assertTrue(self.user.check_password("test123"))
        self.assertEqual(self.user.email, "dalal@example.com")
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.email_verified, False)
    def test_user_points(self):
        """Test that the user points field is initialized correctly."""
        self.assertEqual(self.user.points, 0)
    def test_user_str(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), "dalal")

class GenreModelTest(TestCase):
    """Test case for Genre model."""
    def setUp(self):
        """Create a genre instance for testing."""
        # Create a genre instance with a name
        self.genre = Genre.objects.create(name="Action")
    def test_genre_creation(self):
        """Test that the genre is created with the correct name."""
        self.assertEqual(self.genre.name, "Action")
    def test_genre_str(self):
        """Test the string representation of the genre."""   
        self.assertEqual(str(self.genre), "Action")                     

class ActorModelTest(TestCase):
    """Test case for Actor model."""
    def setUp(self):
        """Create an actor instance for testing."""
        # Create an actor instance with a name and bio
        self.actor = Actor.objects.create(name="Leonardo DiCaprio", biography="An American actor.")
    def test_actor_creation(self):
        """Test that the actor is created with the correct attributes."""
        self.assertEqual(self.actor.name, "Leonardo DiCaprio")
        self.assertEqual(self.actor.biography, "An American actor.")
    def test_actor_str(self):
        """Test the string representation of the actor."""
        self.assertEqual(str(self.actor), "Leonardo DiCaprio")

class DirectorModelTest(TestCase):
    """Test case for Director model."""
    def setUp(self):
        """Create a director instance for testing."""
        self.director = Director.objects.create(name="Christopher Nolan", biography="A British-American director.")
    def test_director_creation(self):
        """Test that the director is created with the correct attributes."""
        self.assertEqual(self.director.name, "Christopher Nolan")
        self.assertEqual(self.director.biography, "A British-American director.")        

class ProducerModelTest(TestCase):
    """Test case for Producer model."""
    def setUp(self):
        """Create a producer instance for testing."""
        self.producer = Producer.objects.create(name="Emma Thomas", biography="A British-American producer.")
    def test_producer_creation(self):
        """Test that the producer is created with the correct attributes."""
        self.assertEqual(self.producer.name, "Emma Thomas")
        self.assertEqual(self.producer.biography, "A British-American producer.")

class MovieModelTest(TestCase):
    """Test case for Movie model."""
    def setUp(self):
        """Create a movie instance for testing."""
        self.genre = Genre.objects.create(name="Action")
        self.director = Director.objects.create(name="Christopher Nolan", biography="A British-American director.")   
        self.producer = Producer.objects.create(name="Emma Thomas", biography="A British-American producer.")
        self.actor = Actor.objects.create(name="Leonardo DiCaprio", biography="An American actor.")
        self.movie = Movie.objects.create(
            title="Inception",
            description="A mind-bending thriller.",
            release_date="2024-01-01",
            rating=8.8,
            director=self.director,
            producer=self.producer,
            poster="path/to/poster.jpg",
            trailer="http://example.com/trailer",
           
        )
        self.movie.genre.add(self.genre)  # Add genre to the movie many-to-many field added by add
        self.movie.actors.add(self.actor)  # Add actor to the movie
    def test_movie_creation(self):
        """Test that the movie is created with the correct attributes."""
        self.assertEqual(self.movie.title, "Inception")
        self.assertEqual(self.movie.description, "A mind-bending thriller.")
        self.assertEqual(self.movie.release_date, "2024-01-01")
        self.assertEqual(self.movie.rating, 8.8)
        self.assertIn(self.genre, self.movie.genre.all())
        self.assertEqual(self.movie.director, self.director)
        self.assertEqual(self.movie.producer, self.producer)
        self.assertEqual(self.movie.poster, "path/to/poster.jpg")
        self.assertEqual(self.movie.trailer, "http://example.com/trailer")
        self.assertEqual(self.movie.actors.count(), 1)
        self.assertEqual(self.movie.actors.first().name, "Leonardo DiCaprio")
    def test_movie_get_genres(self):
        """Test the get_genres method."""
        self.assertEqual(self.movie.get_genres(), "Action")
    def test_movie_str(self):
        """Test the string representation of the movie."""
        self.assertEqual(str(self.movie), "Inception")

class SeatModelTest(TestCase):
    """Test case for Seat model."""
    def setUp(self):
        """Create a seat instance for testing."""
        self.showtime = Showtime.objects.create(
            movie=Movie.objects.create(title="Inception", description="A mind-bending thriller.", release_date="2024-01-01"),
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2)
        )
        self.seat = Seat.objects.create(showtime=self.showtime, seat_number="A1", is_booked=False, price=10.00)
    def test_seat_creation(self):   
        """Test that the seat is created with the correct attributes."""
        self.assertEqual(self.seat.showtime, self.showtime)
        self.assertEqual(self.seat.seat_number, "A1")
        self.assertFalse(self.seat.is_booked)
        self.assertEqual(self.seat.price, 10.00)
    def test_seat_str(self):
        """Test the string representation of the seat."""
        self.assertEqual(str(self.seat), "Inception - Seat A1") 

class ShowtimeModelTest(TestCase):
    """Test case for Showtime model."""
    def setUp(self):
        """Create a showtime instance for testing."""
        self.movie = Movie.objects.create(title="Inception", description="A mind-bending thriller.", release_date="2024-01-01")
        self.auditorium = Auditorium.objects.create(name="Main Auditorium", total_seats=200)

        self.start = make_aware(datetime(2024, 1, 2, 0, 0, 0))
        self.end = make_aware(datetime(2024, 1, 2, 2, 0, 0))

        self.showtime = Showtime.objects.create(
            movie=self.movie,
            start_time=self.start,
            end_time=self.end,
            is_VIP=True,
            thD_available=True,
            parking_available=True,
            language="English",
            auditorium=self.auditorium
        )

    def test_showtime_creation(self):   
        """Test that the showtime is created with the correct attributes."""
        self.assertEqual(self.showtime.movie, self.movie)
        self.assertEqual(self.showtime.start_time.date().strftime("%Y-%m-%d"), (self.start.strftime("%Y-%m-%d")))
        self.assertEqual(self.showtime.end_time.date().strftime(("%Y-%m-%d")), (self.end.strftime("%Y-%m-%d")))
        self.assertTrue(self.showtime.is_VIP)
        self.assertTrue(self.showtime.thD_available)
        self.assertTrue(self.showtime.parking_available)
        self.assertEqual(self.showtime.language, "English")
        self.assertEqual(self.showtime.auditorium, self.auditorium)
    def test_showtime_str(self):
        """Test the string representation of the showtime."""
        self.assertEqual(str(self.showtime), "Inception - 2024-01-02 00:00:00 to 2024-01-02 02:00:00")

class ReviewModelTest(TestCase):
    """Test case for Review model."""
    def setUp(self):
        """Create a review instance for testing.""" 
        self.user = User.objects.create_user(username="dalal", password="test123")
        self.movie = Movie.objects.create(title="Inception", description="A mind-bending thriller.", release_date="2024-01-01")
        self.review = Review.objects.create(user=self.user, movie=self.movie, content="Great movie!", rating=9.0)
    def test_review_creation(self):
        """Test that the review is created with the correct attributes."""
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.movie, self.movie)
        self.assertEqual(self.review.content, "Great movie!")
        self.assertEqual(self.review.rating, 9.0)
    def test_review_str(self):
        """Test the string representation of the review."""
        self.assertEqual(str(self.review), "dalal - Inception Review")

class BookingModelTest(TestCase):
    """Test case for Booking model."""
    def setUp(self):
        self.user = User.objects.create_user(username="dalal", password="test123")
        self.movie = Movie.objects.create(title="Inception", description="Dreams", release_date="2024-01-01")
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2)
        )
       
    def test_booking_creation(self):
        """Test that the booking is created with the correct attributes."""
        booking = Booking.objects.create(user=self.user, showtime=self.showtime, seats=2)
        self.assertEqual(booking.user.username, "dalal")
        self.assertEqual(booking.seats, 2)
        self.assertEqual(str(booking), f"dalal booked {self.movie.title} on {booking.booking_date}")

    def test_booking_cost(self):
        """Test that the booking cost is calculated correctly."""
        booking = Booking.objects.create(user=self.user, showtime=self.showtime, seats=2, cost=20.00)
        self.assertEqual(booking.cost, 20.00)
    def test_booking_str(self):
        """Test the string representation of the booking."""
        booking = Booking.objects.create(user=self.user, showtime=self.showtime, seats=2)
        self.assertEqual(str(booking), f"{self.user.username} booked {self.movie.title} on {booking.booking_date}")


class RoleModelTest(TestCase):
    """Test case for Role model."""
    def setUp(self):
        """Create a role instance for testing."""
        self.actor = Actor.objects.create(name="Leonardo DiCaprio")
        self.movie = Movie.objects.create(title="Inception", description="A mind-bending thriller.", release_date="2024-01-01")
        self.role = Role.objects.create(character_name="Protagonist", actor=self.actor, movie=self.movie)

    def test_role_creation(self):
        """Test that the role is created with the correct attributes."""
        self.assertEqual(self.role.character_name, "Protagonist")
        self.assertEqual(self.role.actor, self.actor)
        self.assertEqual(self.role.movie, self.movie)

    def test_role_str(self):
        """Test the string representation of the role."""
        self.assertEqual(str(self.role),f"{self.actor.name} as {self.role.character_name} in {self.movie.title}")

class TheaterModelTest(TestCase):
    """Test case for Theater model."""
    def setUp(self):
        """Create a theater instance for testing."""
        self.audittoriums =[ Auditorium.objects.create(name="Main Auditorium", total_seats=200),
                            Auditorium.objects.create(name="VIP Auditorium", total_seats=100) ]
        self.theater = Theater.objects.create(name="Cineplex", location="Downtown")
        self.theater.auditoriums.set(self.audittoriums)  # Set the many-to-many relationship
    def test_theater_creation(self):
        """Test that the theater is created with the correct attributes."""
        self.assertEqual(self.theater.name, "Cineplex")
        self.assertEqual(self.theater.location, "Downtown")
        self.assertEqual(self.theater.auditoriums.count(), 2)
        self.assertIn(self.audittoriums[0], self.theater.auditoriums.all())
        self.assertIn(self.audittoriums[1], self.theater.auditoriums.all())
    def test_theater_str(self):
        """Test the string representation of the theater."""
        self.assertEqual(str(self.theater), "Cineplex - Downtown")

class NotificationModelTest(TestCase):
    """Test case for Notification model."""
    def setUp(self):
        """Create a notification instance for testing."""
        self.user = User.objects.create_user(username="dalal", password="test123")
        self.notification = Notification.objects.create(user=self.user, message="Your booking is confirmed.")
    def test_notification_creation(self):
        """Test that the notification is created with the correct attributes."""
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.message, "Your booking is confirmed.")
        self.assertFalse(self.notification.is_read)
    def test_notification_str(self):
        """Test the string representation of the notification."""
        self.assertEqual(str(self.notification), f"Notification for {self.user.username}: Your booking is confirmed.")


class AuditoriumModelTest(TestCase):
    """Test case for Auditorium model."""
    def setUp(self):    
        """Create an auditorium instance for testing."""
        self.theater = Theater.objects.create(name="Cineplex", location="Downtown")
        self.auditorium = Auditorium.objects.create(name="Main Auditorium", total_seats=200, theater=self.theater)
    def test_auditorium_creation(self):
        """Test that the auditorium is created with the correct attributes."""
        self.assertEqual(self.auditorium.name, "Main Auditorium")
        self.assertEqual(self.auditorium.total_seats, 200)
        self.assertEqual(self.auditorium.theater, self.theater)      
    def test_auditorium_str(self):
        """Test the string representation of the auditorium."""
        self.assertEqual(str(self.auditorium), "Main Auditorium - Downtown (200 seats)")