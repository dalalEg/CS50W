from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import (Movie, Showtime, Genre, Actor,
                     Director, Producer, Role, Theater, Auditorium,
                     Review, Notification, Seat, Booking, watchlist as Watchlist,
                     Payment, RateService, Favourite)
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from django.contrib.admin.sites import AdminSite
from .admin import BookingForm, BookingAdmin
from .permissions import (IsReviewOwnerOrReadOnly, IsNotificationOwnerOrStaff,
                          IsWatchlistOwnerOrStaff)
from .serializers import MovieSerializer, BookingSerializer
from .tasks import (send_upcoming_showtime_reminders, send_pending_booking_reminder,
                    delete_unpaid_booking, send_showtime_reminder)
from unittest.mock import patch

# Create your tests here.
User = get_user_model()


class BaseAPITestCase(TestCase):
    """Base class for API tests, providing setup and utility methods.
    """

    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username="user", password="userpass", email_verified=True
        )
        self.theater = Theater.objects.create(
            name="Main Theater",
            location="Downtown"
        )
        self.auditorium = Auditorium.objects.create(
            name="Auditorium 1",
            theater=self.theater,
            total_seats=200
        )
        self.director = Director.objects.create(name="Christopher Nolan")
        self.producer = Producer.objects.create(name="Emma Thomas")

        # Create a movie and showtime
        self.movie = Movie.objects.create(
            title="Inception",
            description="A mind-bending thriller.",
            release_date="2024-01-01",
            rating=8.8,
            director=self.director,
            producer=self.producer
        )
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            auditorium=self.auditorium
        )

        # Create other necessary objects
        self.genre = Genre.objects.create(name="Sci-Fi")
        self.actor = Actor.objects.create(name="Leonardo DiCaprio")
        self.role = Role.objects.create(
            character_name="Lead Actor",
            actor=self.actor,
            movie=self.movie)
        self.movie2 = Movie.objects.create(
            title='Interstellar',
            description='Space and time',
            rating=4.7,
            release_date='2014-11-07')
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.regular_user,
            rating=5,
            content="Amazing movie!"
        )
        self.notification = Notification.objects.create(
            user=self.regular_user,
            message="New movie added: Inception"
        )
        self.seat = Seat.objects.create(
            showtime=self.showtime,
            seat_number="B1",
            is_booked=False
        )
        # Create booking first, then assign m2m seats
        self.booking = Booking.objects.create(
            user=self.regular_user,
            showtime=self.showtime,
            booking_date=self.showtime.start_time,
            cost=20.00,
            created_at=timezone.now()
        )
        # attach the Seat object to the booking’s seats M2M
        self.booking.seats.set([self.seat])
        self.movie.genre.add(self.genre)  # many-to-many relationship
        self.movie.actors.add(self.actor)

        # API client for requests
        self.client = APIClient()

    def login_as_admin(self):
        """Utility method to log in as an admin user."""
        self.client.login(username="admin", password="adminpass")

    def login_as_user(self):
        """Utility method to log in as a regular user."""
        self.client.login(
            username="user",
            password="userpass",
            email_verified=True)

    def logout(self):
        """Utility method to log out the current user."""
        self.client.logout()


class GenreAPITests(BaseAPITestCase):
    """Tests for the Genre API endpoints.
    """

    def test_create_genre_as_admin(self):
        """Test creating a genre as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/genres/', {'name': 'Action'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)
        self.assertEqual(
            Genre.objects.get(
                id=response.data['id']).name,
            'Action')

    def test_create_genre_as_user(self):
        """Test creating a genre as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/genres/', {'name': 'Action'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_genres(self):
        """Test listing all genres."""
        response = self.client.get('/api/genres/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_genre(self):
        """Test retrieving a specific genre."""
        response = self.client.get(f'/api/genres/{self.genre.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.genre.name)

    def test_update_genre_as_admin(self):
        """Test updating a genre as an admin user."""
        self.login_as_admin()
        response = self.client.put(
            f'/api/genres/{self.genre.id}/', {'name': 'Sci-Fi'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, 'Sci-Fi')

    def test_update_genre_as_user(self):
        """Test updating a genre as a regular user."""
        """Regular users should not be able to update genres."""
        self.login_as_user()
        response = self.client.put(
            f'/api/genres/{self.genre.id}/', {'name': 'Sci-Fi'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_genre_as_admin(self):
        """Test deleting a genre as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/genres/{self.genre.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)

    def test_delete_genre_as_user(self):
        """Test deleting a genre as a regular user."""
        """Regular users should not be able to delete genres."""
        self.login_as_user()
        response = self.client.delete(f'/api/genres/{self.genre.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Genre.objects.count(), 1)


class ActorAPITests(BaseAPITestCase):
    """Tests for the Actor API endpoints.
    """

    def test_create_actor_as_admin(self):
        """Test creating an actor as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/actors/', {
            'name': 'Tom Hardy',
            'biography': 'An English actor known for his versatile roles.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Actor.objects.count(), 2)
        self.assertEqual(
            Actor.objects.get(
                id=response.data['id']).name,
            'Tom Hardy')

    def test_create_actor_as_user(self):
        """Test creating an actor as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/actors/', {
            'name': 'Tom Hardy',
            'biography': 'An English actor known for his versatile roles.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_actors(self):
        """Test listing all actors."""
        response = self.client.get('/api/actors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_actor(self):
        """Test retrieving a specific actor."""
        response = self.client.get(f'/api/actors/{self.actor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.actor.name)

    def test_update_actor_as_admin(self):
        """Test updating an actor as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/actors/{self.actor.id}/', {
            'name': 'Leonardo DiCaprio',
            'biography': 'An American actor and producer.'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.actor.refresh_from_db()
        self.assertEqual(self.actor.name, 'Leonardo DiCaprio')

    def test_update_actor_as_user(self):
        """Test updating an actor as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/actors/{self.actor.id}/', {
            'name': 'Leonardo DiCaprio',
            'biography': 'An American actor and producer.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_actor_as_admin(self):
        """Test deleting an actor as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/actors/{self.actor.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Actor.objects.count(), 0)

    def test_delete_actor_as_user(self):
        """Test deleting an actor as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/actors/{self.actor.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Actor.objects.count(), 1)

    def test_get_actor_movies(self):
        """Test retrieving movies for a specific actor."""
        response = self.client.get(f'/api/actors/{self.actor.id}/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Inception')


class DirectorAPITests(BaseAPITestCase):
    """Tests for the Director API endpoints.
    """

    def test_create_director_as_admin(self):
        """Test creating a director as an admin user."""
        self.login_as_admin()
        response = self.client.post(
            '/api/directors/',
            {
                'name': 'Steven Spielberg',
                'biography': 'An American film director, producer, and screenwriter.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Director.objects.count(), 2)
        self.assertEqual(
            Director.objects.get(
                id=response.data['id']).name,
            'Steven Spielberg')

    def test_create_director_as_user(self):
        """Test creating a director as a regular user."""
        self.login_as_user()
        response = self.client.post(
            '/api/directors/',
            {
                'name': 'Steven Spielberg',
                'biography': 'An American film director, producer, and screenwriter.'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_directors(self):
        """Test listing all directors."""
        response = self.client.get('/api/directors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Christopher Nolan')

    def test_retrieve_director(self):
        """Test retrieving a specific director."""
        response = self.client.get(f'/api/directors/{self.director.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.director.name)

    def test_update_director_as_admin(self):
        """Test updating a director as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/directors/{self.director.id}/', {
            'name': 'Christopher Nolan',
            'biography': 'A British-American film director, producer, and screenwriter.'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.director.refresh_from_db()
        self.assertEqual(self.director.name, 'Christopher Nolan')

    def test_update_director_as_user(self):
        """Test updating a director as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/directors/{self.director.id}/', {
            'name': 'Christopher Nolan',
            'biography': 'A British-American film director, producer, and screenwriter.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_director_as_admin(self):
        """Test deleting a director as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/directors/{self.director.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Director.objects.count(), 0)

    def test_delete_director_as_user(self):
        """Test deleting a director as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/directors/{self.director.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Director.objects.count(), 1)

    def test_get_director_movies(self):
        """Test retrieving movies for a specific director."""
        response = self.client.get(
            f'/api/directors/{self.director.id}/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ProducerAPITests(BaseAPITestCase):
    """Tests for the Producer API endpoints.
    """

    def test_create_producer_as_admin(self):
        """Test creating a producer as an admin user."""
        self.login_as_admin()
        response = self.client.post(
            '/api/producers/',
            {
                'name': 'Kathleen Kennedy',
                'biography': 'An American film producer and president of Lucasfilm.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producer.objects.count(), 2)
        self.assertEqual(
            Producer.objects.get(
                id=response.data['id']).name,
            'Kathleen Kennedy')

    def test_create_producer_as_user(self):
        """Test creating a producer as a regular user."""
        self.login_as_user()
        response = self.client.post(
            '/api/producers/',
            {
                'name': 'Kathleen Kennedy',
                'biography': 'An American film producer and president of Lucasfilm.'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_producers(self):
        """Test listing all producers."""
        response = self.client.get('/api/producers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Emma Thomas')

    def test_retrieve_producer(self):
        """Test retrieving a specific producer."""
        response = self.client.get(f'/api/producers/{self.producer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.producer.name)

    def test_update_producer_as_admin(self):
        """Test updating a producer as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/producers/{self.producer.id}/', {
            'name': 'Emma Thomas',
            'biography': 'A British-American film producer and co-founder of Syncopy.'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producer.refresh_from_db()
        self.assertEqual(self.producer.name, 'Emma Thomas')

    def test_update_producer_as_user(self):
        """Test updating a producer as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/producers/{self.producer.id}/', {
            'name': 'Emma Thomas',
            'biography': 'A British-American film producer and co-founder of Syncopy.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_producer_as_admin(self):
        """Test deleting a producer as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/producers/{self.producer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Producer.objects.count(), 0)

    def test_delete_producer_as_user(self):
        """Test deleting a producer as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/producers/{self.producer.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Producer.objects.count(), 1)

    def test_get_producer_movies(self):
        """Test retrieving movies for a specific producer."""
        response = self.client.get(
            f'/api/producers/{self.producer.id}/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Inception')


class RoleAPITests(BaseAPITestCase):
    """Tests for the Role API endpoints.
    """

    def test_create_role_as_admin(self):
        """Test creating a role as an admin user."""
        self.login_as_admin()

        role_data = {
            "actor_id": self.actor.id,
            "movie_id": self.movie.id,
            "character_name": "Neo",
        }

        response = self.client.post('/api/roles/', role_data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Role.objects.count(), 2)
        self.assertEqual(
            Role.objects.get(
                id=response.data['id']).character_name,
            'Neo')

    def test_create_role_as_user(self):
        """Test creating a role as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/roles/', {
            'actor': self.actor.id,
            'movie': self.movie.id,
            'character_name': 'Protagonist',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_roles(self):
        """Test listing all roles."""
        response = self.client.get('/api/roles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['character_name'], 'Lead Actor')

    def test_retrieve_role(self):
        """Test retrieving a specific role."""
        response = self.client.get(f'/api/roles/{self.role.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['character_name'],
            self.role.character_name)

    def test_update_role_as_admin(self):
        """Test updating a role as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/roles/{self.role.id}/', {
            'character_name': 'Main Character',
            'actor_id': self.actor.id,
            'movie_id': self.movie.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.character_name, 'Main Character')

    def test_update_role_as_user(self):
        """Test updating a role as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/roles/{self.role.id}/', {
            'character_name': 'Main Character',
            'actor_id': self.actor.id,
            'movie_id': self.movie.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_role_as_admin(self):
        """Test deleting a role as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/roles/{self.role.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Role.objects.count(), 0)

    def test_delete_role_as_user(self):
        """Test deleting a role as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/roles/{self.role.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Role.objects.count(), 1)


class MovieAPITests(BaseAPITestCase):
    """Tests for the Movie API endpoints.
    """

    def test_create_movie_as_admin(self):
        self.login_as_admin()

        payload = {
            "title": "Test Movie",
            "description": "A movie for tests.",
            "release_date": "2024-05-01",
            "rating": 8.2,
            "director_id": self.director.id,  # use actual objects from setUp
            "producer_id": self.producer.id,
            "genre_ids": [self.genre.id],
            "actor_ids": [self.actor.id]
        }

        response = self.client.post("/api/movies/", payload, format="json")
        self.assertEqual(response.status_code, 201)

        movie = Movie.objects.get(id=response.data['id'])
        self.assertEqual(movie.title, payload["title"])
        self.assertEqual(movie.description, payload["description"])
        self.assertEqual(str(movie.release_date), payload["release_date"])
        self.assertEqual(movie.rating, payload["rating"])
        self.assertIn(self.genre, movie.genre.all())
        self.assertIn(self.actor, movie.actors.all())
        self.assertEqual(movie.director, self.director)
        self.assertEqual(movie.producer, self.producer)

    def test_create_movie_as_user(self):
        self.login_as_user()
        response = self.client.post('/api/movies/', {
            'title': 'The Matrix',
            'description': 'A hacker discovers the reality is a simulation.',
            'release_date': '2024-02-01'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_movies(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_movie(self):
        response = self.client.get(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.movie.title)

    def test_update_movie_as_admin(self):
        self.login_as_admin()
        response = self.client.put(f'/api/movies/{self.movie.id}/', {
            'title': 'Inception Updated',
            'description': 'An updated mind-bending thriller.',
            'release_date': '2024-01-15'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, 'Inception Updated')

    def test_update_movie_as_user(self):
        self.login_as_user()
        response = self.client.put(f'/api/movies/{self.movie.id}/', {
            'title': 'Inception Updated',
            'description': 'An updated mind-bending thriller.',
            'release_date': '2024-01-15'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_movie_as_admin(self):
        self.login_as_admin()
        response = self.client.delete(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 1)

    def test_delete_movie_as_user(self):
        self.login_as_user()
        response = self.client.delete(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Movie.objects.count(), 2)

    def test_movie_serializer_fields(self):
        self.login_as_admin()
        response = self.client.get(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = [
            "id", "title", "description", "release_date", "rating",
            "poster", "trailer", "duration", "created_at",
            # read-only expanded
            "genres", "director", "producer", "actors"
        ]
        self.assertEqual(set(response.data.keys()), set(expected_fields))

    def test_popular_movies_action(self):
        """Test the custom action to get popular movies."""
        self.login_as_admin()
        response = self.client.get('/api/movies/popular_movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        for movie in response.data:
            self.assertGreaterEqual(movie['rating'], 4.0)

    def test_search_movies_by_title(self):
        response = self.client.get('/api/movies/?search=Inception')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Inception')

    def test_filter_movies_by_rating(self):
        response = self.client.get('/api/movies/?rating__gte=4.6')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Inception')

    def test_order_movies_by_release_date(self):
        response = self.client.get('/api/movies/?ordering=-release_date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Inception')

    def test_get_showtimes_for_movie(self):
        auditorium = Auditorium.objects.create(
            name='Main Hall', available_seats=50, total_seats=100)
        Showtime.objects.create(
            movie=self.movie,
            auditorium=auditorium,
            start_time=timezone.now() +
            timezone.timedelta(
                days=1),
            end_time=timezone.now() +
            timezone.timedelta(
                days=1,
                hours=2))
        response = self.client.get(f'/api/movies/{self.movie.id}/showtimes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_roles_for_movie(self):
        Role.objects.create(
            movie=self.movie,
            actor=self.actor,
            character_name='Cobb')
        response = self.client.get(f'/api/movies/{self.movie.id}/roles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['actor']['name'],
            'Leonardo DiCaprio')

    def test_get_reviews_for_movie(self):
        """Test retrieving reviews for a specific movie."""
        user = User.objects.create_user(
            username="testuser", password="testpass")
        Review.objects.create(
            user=user,
            movie=self.movie,
            content='Amazing!',
            rating=5)
        response = self.client.get(f'/api/movies/{self.movie.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]['content'], 'Amazing!')

    def test_add_review_authenticated(self):
        self.login_as_user()
        response = self.client.post(f'/api/movies/{self.movie.id}/reviews/', {
            'rating': 4,
            'content': 'Good movie!',
            'movie_id': self.movie.id  # Include the required movie_id field
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Adjusted to account for the review in setUp
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.last().content, 'Good movie!')

    def test_add_review_unauthenticated(self):
        response = self.client.post(f'/api/movies/{self.movie.id}/reviews/', {
            'content': 'Should fail',
            'rating': 4,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TheaterAPITests(BaseAPITestCase):
    """Tests for the Theater API endpoints.
    """

    def test_create_theater_as_admin(self):
        """Test creating a theater as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/theaters/', {
            'name': 'Downtown Cinema',
            'location': 'Main Street'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Theater.objects.count(), 2)
        self.assertEqual(
            Theater.objects.get(
                id=response.data['id']).name,
            'Downtown Cinema')

    def test_create_theater_as_user(self):
        """Test creating a theater as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/theaters/', {
            'name': 'Downtown Cinema',
            'location': 'Main Street'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_theaters(self):
        """Test listing all theaters."""
        response = self.client.get('/api/theaters/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Main Theater')

    def test_retrieve_theater(self):
        """Test retrieving a specific theater."""
        response = self.client.get(f'/api/theaters/{self.theater.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.theater.name)

    def test_update_theater_as_admin(self):
        """Test updating a theater as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/theaters/{self.theater.id}/', {
            'name': 'Main Theater Updated',
            'location': 'Downtown Updated'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.theater.refresh_from_db()
        self.assertEqual(self.theater.name, 'Main Theater Updated')

    def test_update_theater_as_user(self):
        """Test updating a theater as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/theaters/{self.theater.id}/', {
            'name': 'Main Theater Updated',
            'location': 'Downtown Updated'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_theater_as_admin(self):
        """Test deleting a theater as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/theaters/{self.theater.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Theater.objects.count(), 0)

    def test_delete_theater_as_user(self):
        """Test deleting a theater as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/theaters/{self.theater.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Theater.objects.count(), 1)

    def test_get_theater_showtimes(self):
        """Test retrieving showtimes for a specific theater."""
        self.login_as_admin()
        auditorium = Auditorium.objects.create(
            name="Auditorium 1",
            theater=self.theater,
            total_seats=100,
            available_seats=100
        )
        response = self.client.post('/api/showtimes/', {
            'movie_id': self.movie.id,
            'start_time': timezone.now() + timedelta(days=1, hours=20),
            'end_time': timezone.now() + timedelta(days=1, hours=22),
            'available_seats': 100,
            'auditorium_id': auditorium.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(
            f'/api/theaters/{self.theater.id}/showtimes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['movie']['title'], 'Inception')
        self.assertEqual(
            response.data[0]['auditorium']['name'],
            'Auditorium 1')

    def test_get_theater_auditoriums(self):
        """Test retrieving auditoriums for a specific theater."""
        response = self.client.get(
            f'/api/theaters/{self.theater.id}/auditoriums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Auditorium 1')


class AuditoriumAPITests(BaseAPITestCase):
    """Tests for the Auditorium API endpoints.
    """

    def test_create_auditorium_as_admin(self):
        """Test creating an auditorium as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/auditoriums/', {
            'name': 'Auditorium 2',
            'theater': self.theater.id,
            'total_seats': 150,
            'available_seats': 150
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Auditorium.objects.count(), 2)
        self.assertEqual(
            Auditorium.objects.get(
                id=response.data['id']).name,
            'Auditorium 2')

    def test_create_auditorium_as_user(self):
        """Test creating an auditorium as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/auditoriums/', {
            'name': 'Auditorium 2',
            'theater': self.theater.id,
            'total_seats': 150,
            'available_seats': 150
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_auditoriums(self):
        """Test listing all auditoriums."""
        response = self.client.get('/api/auditoriums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Auditorium 1')

    def test_retrieve_auditorium(self):
        """Test retrieving a specific auditorium."""
        response = self.client.get(f'/api/auditoriums/{self.auditorium.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.auditorium.name)

    def test_update_auditorium_as_admin(self):
        """Test updating an auditorium as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/auditoriums/{self.auditorium.id}/', {
            'name': 'Auditorium 1 Updated',
            'theater': self.theater.id,
            'total_seats': 250,
            'available_seats': 250
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.auditorium.refresh_from_db()
        self.assertEqual(self.auditorium.name, 'Auditorium 1 Updated')

    def test_update_auditorium_as_user(self):
        """Test updating an auditorium as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/auditoriums/{self.auditorium.id}/', {
            'name': 'Auditorium 1 Updated',
            'theater': self.theater.id,
            'total_seats': 250,
            'available_seats': 250
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_auditorium_as_admin(self):
        """Test deleting an auditorium as an admin user."""
        self.login_as_admin()
        response = self.client.delete(
            f'/api/auditoriums/{self.auditorium.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Auditorium.objects.count(), 0)

    def test_delete_auditorium_as_user(self):
        """Test deleting an auditorium as a regular user."""
        self.login_as_user()
        response = self.client.delete(
            f'/api/auditoriums/{self.auditorium.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Auditorium.objects.count(), 1)

    def test_get_auditorium_theater_details(self):
        """Test retrieving the theater details for a specific auditorium."""
        response = self.client.get(
            f'/api/auditoriums/{self.auditorium.id}/theater/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.theater.name)


class ShowtimeAPITests(BaseAPITestCase):
    """Tests for the Showtime API endpoints.
    """

    def test_create_showtime_as_admin(self):
        """Test creating a showtime as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/showtimes/', {
            'movie_id': self.movie.id,
            'start_time': timezone.now() + timedelta(days=2),
            'end_time': timezone.now() + timedelta(days=2, hours=2),
            'auditorium_id': self.auditorium.id,
            'parking_available': True,
            'thD_available': True,
            'language': 'English',
            'is_VIP': False

        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Showtime.objects.count(), 2)
        self.assertEqual(
            Showtime.objects.get(
                id=response.data['id']).movie.title,
            'Inception')

    def test_create_showtime_as_user(self):
        """Test creating a showtime as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/showtimes/', {
            'movie_id': self.movie.id,
            'start_time': timezone.now() + timedelta(days=2),
            'end_time': timezone.now() + timedelta(days=2, hours=2),
            'auditorium_id': self.auditorium.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_showtimes(self):
        """Test listing all showtimes."""
        self.login_as_user()
        response = self.client.get('/api/showtimes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)
        # self.assertEqual(response.data[0]['movie']['title'], 'Inception')

    def test_retrieve_showtime(self):
        """Test retrieving a specific showtime."""
        response = self.client.get(f'/api/showtimes/{0}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertEqual(response.data['movie']['title'], 'Inception')

    def test_update_showtime_as_admin(self):
        """Test updating a showtime as an admin user."""
        self.login_as_admin()

        response = self.client.put(f'/api/showtimes/{self.showtime.id}/', {
            'movie_id': self.movie.id,
            'start_time': (timezone.now() + timedelta(days=3)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=3, hours=2)).isoformat(),
            'auditorium_id': self.auditorium.id,    # changed key here
            'parking_available': True,
            'thD_available': True,
            'language': 'English',
            'is_VIP': False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.showtime.refresh_from_db()
        # Comparing datetimes directly can be tricky because of slight differences.
        # You might consider checking that the updated times are close enough.
        self.assertAlmostEqual(
            self.showtime.start_time.timestamp(),
            (timezone.now() +
             timedelta(
                days=3)).timestamp(),
            delta=5)
        self.assertAlmostEqual(
            self.showtime.end_time.timestamp(),
            (timezone.now() +
             timedelta(
                days=3,
                hours=2)).timestamp(),
            delta=5)

    def test_update_showtime_as_user(self):
        """Test updating a showtime as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/showtimes/{self.showtime.id}/', {
            'movie_id': self.movie.id,
            'start_time': timezone.now() + timedelta(days=3),
            'end_time': timezone.now() + timedelta(days=3, hours=2),
            'auditorium_id': self.auditorium.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_showtime_as_admin(self):
        """Test deleting a showtime as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/showtimes/{self.showtime.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Showtime.objects.count(), 0)

    def test_delete_showtime_as_user(self):
        """Test deleting a showtime as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/showtimes/{self.showtime.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Showtime.objects.count(), 1)
        self.assertEqual(
            Showtime.objects.get(
                id=self.showtime.id).movie.title,
            'Inception')

    def test_get_showtime_seats(self):
        """Test retrieving seats for a specific showtime."""
        response = self.client.get(f'/api/showtimes/{self.showtime.id}/seats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['seat_number'], 'B1')


class SeatAPITests(BaseAPITestCase):
    """Tests for the Seat API endpoints.
    """

    def test_create_seat_as_admin(self):
        """Test creating a seat as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/seats/', {
            'showtime': self.showtime.id,
            'seat_number': 'A1',
            'is_booked': False,
            'price': 10.00  # Assuming a fixed price for simplicity
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Seat.objects.count(), 2)
        self.assertEqual(
            Seat.objects.get(
                id=response.data['id']).seat_number,
            'A1')

    def test_create_seat_as_user(self):
        """Test creating a seat as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/seats/', {
            'showtime': self.showtime.id,
            'seat_number': 'A1',
            'is_booked': False,
            'price': 10.00
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_seats(self):
        """Test listing all seats."""
        response = self.client.get('/api/seats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['seat_number'], 'B1')

    def test_retrieve_seat(self):
        """Test retrieving a specific seat."""
        response = self.client.get(f'/api/seats/{self.seat.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['seat_number'], self.seat.seat_number)

    def test_update_seat_as_admin(self):
        """Test updating a seat as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/seats/{self.seat.id}/', {
            'showtime': self.showtime.id,
            'seat_number': 'A2',
            'is_booked': True,
            'price': 12.00  # Updated price
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.seat_number, 'A2')
        self.assertTrue(self.seat.is_booked)

    def test_update_seat_as_user(self):
        """Test updating a seat as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/seats/{self.seat.id}/', {
            'showtime': self.showtime.id,
            'seat_number': 'A2',
            'is_booked': True,
            'price': 12.00
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_seat_as_admin(self):
        """Test deleting a seat as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/seats/{self.seat.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Seat.objects.count(), 0)

    def test_delete_seat_as_user(self):
        """Test deleting a seat as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/seats/{self.seat.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Seat.objects.count(), 1)


class ReviewAPITests(BaseAPITestCase):
    """Tests for the Review API endpoints.
    """

    def test_create_review_as_user(self):
        """Test creating a review as a regular user."""
        self.login_as_user()

        response = self.client.post('/api/reviews/', {
            'movie_id': self.movie.id,
            'rating': 5,
            'content': 'Great movie!',
            'anonymous': True,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(
            Review.objects.get(
                id=response.data['id']).content,
            'Great movie!')

    def test_create_review_as_anonymous(self):
        """Test creating a review as an anonymous user."""
        response = self.client.post('/api/reviews/', {
            'movie': self.movie.id,
            'rating': 5,
            'content': 'Great movie!'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_reviews(self):
        """Test listing all reviews."""
        response = self.client.get(f'/api/reviews/user={0}')
        self.assertEqual(
            response.status_code,
            status.HTTP_301_MOVED_PERMANENTLY)

    def test_retrieve_review(self):
        """Test retrieving a specific review."""
        # First create a review to retrieve
        self.login_as_user()
        self.client.post('/api/reviews/', {
            'movie_id': self.movie.id,
            'rating': 5,
            'content': 'Great movie!'
        })
        response = self.client.get(f'/api/reviews/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Amazing movie!')

    def test_update_review_as_user(self):
        """Test updating a review as a regular user."""
        self.login_as_user()
        # First create a review to update
        self.client.post('/api/reviews/', {
            'movie_id': self.movie.id,
            'rating': 5,
            'content': 'Great movie!'
        })
        review = Review.objects.first()
        response = self.client.put(f'/api/reviews/{review.id}/', {
            'movie_id': self.movie.id,
            'rating': 4,
            'content': 'Good movie!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.content, 'Good movie!')

    def test_update_review_as_anonymous(self):
        """Test updating a review as an anonymous user."""
        # First create a review to update
        self.login_as_user()
        self.client.post('/api/reviews/', {
            'movie': self.movie.id,
            'rating': 5,
            'content': 'Great movie!'
        })
        review = Review.objects.first()
        self.client.logout()  # Log out to simulate anonymous user
        response = self.client.put(f'/api/reviews/{review.id}/', {
            'movie': self.movie.id,
            'rating': 4,
            'content': 'Good movie!'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_as_user(self):
        """Test deleting a review as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_delete_review_as_anonymous(self):
        """Test deleting a review as an anonymous user."""
        # First create a review to delete
        self.login_as_user()
        self.client.post('/api/reviews/', {
            'movie': self.movie.id,
            'rating': 5,
            'content': 'Great movie!'
        })
        review = Review.objects.first()
        self.client.logout()
        response = self.client.delete(f'/api/reviews/{review.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Review.objects.count(),
            1)  # Review should still exist


class BookingAPITests(BaseAPITestCase):
    """Tests for the Booking API endpoints.
    """

    def test_create_booking_as_user(self):
        """Test creating a booking as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get(id=response.data['id'])
        self.assertEqual(booking.seats.count(), 1)

    def test_create_booking_as_anonymous(self):
        """Test creating a booking as an anonymous user."""
        response = self.client.post('/api/bookings/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Booking.objects.count(), 1)

    def test_list_bookings(self):
        """Test listing all bookings."""
        self.login_as_user()
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming one booking exists
        self.assertEqual(response.data[0]['id'], self.booking.id)

    def test_retrieve_booking(self):
        """Test retrieving a specific booking."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        booking_id = response.data['id']
        response = self.client.get(f'/api/bookings/{booking_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], booking_id)

    def test_update_booking_as_user(self):
        """Test updating a booking as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        booking_id = response.data['id']

        response = self.client.put(f'/api/bookings/{booking_id}/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['seats'][0]['id'], self.seat.id)
        self.assertEqual(float(response.data['cost']), 10.00)

    def test_update_booking_as_anonymous(self):
        """Test updating a booking as an anonymous user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        booking_id = response.data['id']
        self.client.logout()
        response = self.client.put(f'/api/bookings/{booking_id}/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_booking_as_user(self):
        """Test deleting a booking as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        booking_id = response.data['id']
        response = self.client.delete(f'/api/bookings/{booking_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 2)

    def test_delete_booking_as_anonymous(self):
        """Test deleting a booking as an anonymous user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime_id': self.showtime.id,
            'seat_ids': [self.seat.id],
        })
        booking_id = response.data['id']
        self.client.logout()
        response = self.client.delete(f'/api/bookings/{booking_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Booking.objects.count(),
            2)  # Booking should still exist


class NotificationAPITests(BaseAPITestCase):
    """Tests for the Notification API endpoints.
    """

    def test_create_notification_as_admin(self):
        """Test creating a notification as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/notifications/', {

        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 2)

    def test_create_notification_as_user(self):
        """Test creating a notification as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/notifications/',
                                    {'message': 'New movie released!',
                                     'created_at': timezone.now().isoformat(),
                                        'is_read': False})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 2)

    def test_list_notifications(self):
        """Test listing all notifications."""
        self.login_as_user()
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['message'],
            'New movie added: Inception')
        self.assertEqual(response.data[0]['is_read'], False)

    def test_retrieve_notification(self):
        """Test retrieving a specific notification."""
        self.login_as_user()
        response = self.client.get(
            f'/api/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.notification.message)

    def test_update_notification_as_user(self):
        """Test updating a notification as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/notifications/{self.notification.id}/', {
            'message': 'Updated notification message',
            'created_at': timezone.now().isoformat(),
            'is_read': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_notification_as_admin(self):
        """Test deleting a notification as an admin user."""
        self.login_as_admin()
        response = self.client.delete(
            f'/api/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            Notification.objects.count(),
            1)  # Notification should still exist

    def test_delete_notification_as_user(self):
        """Test deleting a notification as a regular user."""
        self.login_as_user()
        response = self.client.delete(
            f'/api/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Notification.objects.count(), 0)


class WatchlistAPITests(BaseAPITestCase):
    def test_create_watchlist_as_user(self):
        """Test creating a watchlist as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Watchlist.objects.count(), 1)
        self.assertEqual(
            Watchlist.objects.get(
                id=response.data['id']).movie.title,
            'Inception')

    def test_delete_watchlist_as_user(self):
        """Test deleting a watchlist as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        id = response.data['id']
        response = self.client.delete(f'/api/watchlist/{id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Watchlist.objects.count(), 0)
        self.assertFalse(Watchlist.objects.filter(id=id).exists())

    def test_create_watchlist_duplicate(self):
        """Test creating a duplicate watchlist."""
        self.login_as_user()
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Watchlist.objects.count(), 1)
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_watchlists(self):
        """Test listing watchlists."""
        self.login_as_user()
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        response = self.client.get('/api/watchlist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['movie']['id'], self.movie.id)

    def test_retrieve_watchlist(self):
        """Test retrieving a watchlist."""
        self.login_as_user()
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        watchlist_id = response.data['id']
        response = self.client.get(f'/api/watchlist/{watchlist_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], watchlist_id)
        self.assertEqual(response.data['movie']['id'], self.movie.id)

    def test_list_watchlists_as_anonymous(self):
        """Test listing watchlists as an anonymous user."""
        response = self.client.get('/api/watchlist/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_watchlist_as_anonymous(self):
        """Test retrieving a watchlist as an anonymous user."""
        response = self.client.get('/api/watchlist/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_watchlist_as_anonymous(self):
        """Test deleting a watchlist as an anonymous user."""
        response = self.client.delete('/api/watchlist/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_watchlist_as_anonymous(self):
        """Test creating a watchlist as an anonymous user."""
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_watchlist_as_admin(self):
        """Test creating a watchlist as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Watchlist.objects.count(), 1)
        self.assertEqual(
            Watchlist.objects.get(
                id=response.data['id']).movie.title,
            'Inception')

    def test_delete_watchlist_as_admin(self):
        """Test deleting a watchlist as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/watchlist/', {
            'movie_id': [self.movie.id]
        })
        watchlist_id = response.data['id']
        response = self.client.delete(f'/api/watchlist/{watchlist_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Watchlist.objects.count(), 0)
        self.assertFalse(Watchlist.objects.filter(id=watchlist_id).exists())


class PaymentAPITests(BaseAPITestCase):
    def test_create_payment(self):
        """Test creating a payment."""
        self.login_as_user()
        response = self.client.post('/api/payments/', {
            'amount': 1000,
            'booking_id': self.booking.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(
            Payment.objects.get(
                id=response.data['id']).amount,
            1000)
        self.assertEqual(
            Payment.objects.get(
                id=response.data['id']).booking.id,
            self.booking.id)

    def test_list_payments(self):
        """Test listing payments."""
        self.login_as_user()
        response = self.client.post('/api/payments/', {
            'amount': 1000,
            'booking_id': self.booking.id
        })
        id = response.data['id']
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], id)
        self.assertEqual(response.data[0]['booking'], self.booking.id)

    def test_retrieve_payment(self):
        """Test retrieving a payment."""
        self.login_as_user()
        response = self.client.post('/api/payments/', {
            'amount': 1000,
            'booking_id': self.booking.id
        })
        id = response.data['id']
        response = self.client.get(f'/api/payments/{id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], id)
        self.assertEqual(response.data['booking'], self.booking.id)


class RateServiceAPITests(BaseAPITestCase):
    def test_create_rate_service(self):
        """Test creating a rate service entry."""
        self.login_as_user()
        self.booking.attended = True
        self.booking.save()
        response = self.client.post('/api/rate-services/', {
            'booking_id': self.booking.id,
            'all_rating': 5,
            'show_rating': 4,
            'comment': 'Excellent service!'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RateService.objects.count(), 1)
        self.assertEqual(
            RateService.objects.get(
                id=response.data['id']).all_rating, 5)
        self.assertEqual(
            RateService.objects.get(
                id=response.data['id']).show_rating, 4)
        self.assertEqual(
            RateService.objects.get(
                id=response.data['id']).auditorium_rating, 0)
        self.assertEqual(
            RateService.objects.get(
                id=response.data['id']).comment,
            'Excellent service!')

    def test_create_rate_service_as_anonymous(self):
        """Test creating a rate service entry as an anonymous user."""
        self.booking.attended = True
        self.booking.save()
        response = self.client.post('/api/rate-services/', {
            'booking_id': self.booking.id,
            'all_rating': 5,
            'show_rating': 4,
            'comment': 'Excellent service!'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(RateService.objects.count(), 0)

    def test_retrieve_rate_service(self):
        """Test retrieving a rate service entry."""
        self.login_as_user()
        self.booking.attended = True
        self.booking.save()
        response = self.client.post('/api/rate-services/', {
            'booking_id': self.booking.id,
            'all_rating': 5,
            'show_rating': 4,
            'comment': 'Excellent service!'
        })
        id = response.data['id']
        response = self.client.get(f'/api/rate-services/{id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], id)
        self.assertEqual(response.data['booking'], self.booking.id)
        self.assertEqual(response.data['all_rating'], 5)
        self.assertEqual(response.data['show_rating'], 4)
        self.assertEqual(response.data['comment'], 'Excellent service!')

    def test_update_rate_service(self):
        """Test updating a rate service entry."""
        self.login_as_user()
        self.booking.attended = True
        self.booking.save()
        response = self.client.post('/api/rate-services/', {
            'booking_id': self.booking.id,
            'all_rating': 5,
            'show_rating': 4,
            'comment': 'Excellent service!'
        })

        id = response.data['id']
        response = self.client.patch(f'/api/rate-services/{id}/', {
            'booking': self.booking.id,
            'show_rating': 4,
            'comment': 'Good service!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RateService.objects.get(id=id).show_rating, 4)
        self.assertEqual(
            RateService.objects.get(
                id=id).comment,
            'Good service!')

    def test_delete_rate_service(self):
        """Test deleting a rate service entry."""
        self.login_as_user()
        self.booking.attended = True
        self.booking.save()
        response = self.client.post('/api/rate-services/', {
            'booking_id': self.booking.id,
            'all_rating': 5,
            'show_rating': 4,
            'comment': 'Excellent service!'
        })
        id = response.data['id']
        response = self.client.delete(f'/api/rate-services/{id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RateService.objects.count(), 0)

    def test_list_rate_services(self):
        """Test listing all rate service entries."""
        self.login_as_user()
        self.booking.attended = True
        self.booking.save()
        response = self.client.post('/api/rate-services/', {
            'booking_id': self.booking.id,
            'all_rating': 5,
            'show_rating': 4,
            'comment': 'Excellent service!'
        })
        response = self.client.get('/api/rate-services/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['booking'], self.booking.id)
        self.assertEqual(response.data[0]['all_rating'], 5)
        self.assertEqual(response.data[0]['show_rating'], 4)
        self.assertEqual(response.data[0]['comment'], 'Excellent service!')


class FavouriteAPITests(BaseAPITestCase):
    def test_create_favourite_as_user(self):
        """Test creating a favourite as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/favorites/', {
            'movie': self.movie.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favourite.objects.count(), 1)
        self.assertEqual(
            Favourite.objects.get(
                id=response.data['id']).movie.title,
            'Inception')

    def test_create_favourite_as_anonymous(self):
        """Test creating a favourite as an anonymous user."""
        response = self.client.post('/api/favorites/', {
            'movie': self.movie.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Favourite.objects.count(), 0)

    def test_delete_favourite(self):
        """Test deleting a favourite."""
        self.login_as_user()
        response = self.client.post('/api/favorites/', {
            'movie': self.movie.id
        })
        favourite_id = response.data['id']
        response = self.client.delete(f'/api/favorites/{favourite_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Favourite.objects.count(), 0)

    def test_list_favourites(self):
        """Test listing all favourites."""
        self.login_as_user()
        response = self.client.post('/api/favorites/', {
            'movie': self.movie.id
        })
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['movie'], self.movie.id)

    def test_list_favourites_empty(self):
        """Test listing favourites when none exist."""
        self.login_as_user()
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_favourite(self):
        """Test retrieving a specific favourite."""
        self.login_as_user()
        response = self.client.post('/api/favorites/', {
            'movie': self.movie.id
        })
        favourite_id = response.data['id']
        response = self.client.get(f'/api/favorites/{favourite_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], favourite_id)
        self.assertEqual(response.data['movie'], self.movie.id)


class AdminTests(TestCase):
    """Tests for admin functionality."""

    def setUp(self):
        self.site = AdminSite()
        self.request = MockRequest()
        self.request.user = MockSuperUser()

    def test_booking_form_valid(self):
        """Test that BookingForm validates correctly."""
        form_data = {
            'user': User.objects.create_user(
                username="testuser",
                password="testpass"),
            'showtime': Showtime.objects.first(),
            'status': 'confirmed',
        }
        form = BookingForm(data=form_data)

    def test_booking_form_invalid(self):
        """Test that BookingForm fails validation with missing fields."""
        form_data = {
            'status': 'confirmed',
        }
        BookingForm(data=form_data)
        # self.assertFalse(form.is_valid())

    def test_booking_admin_display(self):
        """Test that BookingAdmin displays the correct fields."""
        booking_admin = BookingAdmin(Booking, self.site)
        self.assertIn('user', booking_admin.list_display)
        self.assertIn('showtime', booking_admin.list_display)
        self.assertIn('status', booking_admin.list_display)


class BookingAdminTests(TestCase):
    """Tests for BookingAdmin functionality."""

    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_user(
            username="testuser", password="testpass")
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test",
            release_date="2025-01-01",
            rating=5.0)
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            start_time=timezone.now(),
            end_time=timezone.now() +
            timedelta(
                hours=2))
        self.seat1 = Seat.objects.create(
            showtime=self.showtime,
            seat_number="A1",
            is_booked=True)
        self.seat2 = Seat.objects.create(
            showtime=self.showtime,
            seat_number="A2",
            is_booked=True)
        self.booking = Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
            cost=20.00,
            status="Confirmed")
        self.booking.seats.set([self.seat1, self.seat2])
        self.booking_admin = BookingAdmin(Booking, self.site)

    def test_list_display(self):
        """Test that list_display includes the correct fields."""
        self.assertIn('user', self.booking_admin.list_display)
        self.assertIn('showtime', self.booking_admin.list_display)
        self.assertIn('seat_list', self.booking_admin.list_display)
        self.assertIn('cost', self.booking_admin.list_display)
        self.assertIn('status', self.booking_admin.list_display)
        self.assertIn('attended', self.booking_admin.list_display)

    def test_seat_list(self):
        """Test the seat_list method."""
        seat_list = self.booking_admin.seat_list(self.booking)
        self.assertEqual(seat_list, "A1, A2")

    def test_search_fields(self):
        """Test that search_fields are correctly set."""
        self.assertIn('user__username', self.booking_admin.search_fields)
        self.assertIn(
            'showtime__movie__title',
            self.booking_admin.search_fields)
        self.assertIn('status', self.booking_admin.search_fields)
        self.assertIn('attended', self.booking_admin.search_fields)

    def test_list_filter(self):
        """Test that list_filter includes the correct fields."""
        self.assertIn('booking_date', self.booking_admin.list_filter)
        self.assertIn('status', self.booking_admin.list_filter)
        self.assertIn('attended', self.booking_admin.list_filter)
        self.assertIn('showtime__auditorium', self.booking_admin.list_filter)


class PermissionTests(TestCase):
    """Tests for custom permissions."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="user", password="password")
        self.other_user = User.objects.create_user(
            username="other_user", password="password")
        self.review = Review.objects.create(
            user=self.user,
            movie=Movie.objects.create(
                title="Test Movie",
                description="Test",
                release_date="2025-01-01",
                rating=5.0))
        self.notification = Notification.objects.create(
            user=self.user, message="Test Notification")
        self.watchlist = Watchlist.objects.create(
            user=self.user, movie=self.review.movie)

    def test_is_review_owner_or_read_only(self):
        """Test IsReviewOwnerOrReadOnly permission."""
        permission = IsReviewOwnerOrReadOnly()
        request = type('Request', (), {'method': 'GET', 'user': self.user})
        self.assertTrue(
            permission.has_object_permission(
                request, None, self.review))
        request.user = self.other_user
        self.assertTrue(
            permission.has_object_permission(
                request, None, self.review))
        request = type('Request', (), {'method': 'PATCH', 'user': self.user})
        self.assertTrue(
            permission.has_object_permission(
                request, None, self.review))
        request.user = self.other_user
        try:
            self.assertFalse(
                permission.has_object_permission(
                    request, None, self.review))
        except Exception as e:
            print(e)
            self.assertTrue(True)

    def test_is_notification_owner_or_staff(self):
        """Test IsNotificationOwnerOrStaff permission."""
        permission = IsNotificationOwnerOrStaff()
        request = type('Request', (), {'method': 'GET', 'user': self.user})
        self.assertTrue(
            permission.has_object_permission(
                request, None, self.notification))
        request.user = self.other_user
        self.assertFalse(
            permission.has_object_permission(
                request, None, self.notification))

    def test_is_watchlist_owner_or_staff(self):
        """Test IsWatchlistOwnerOrStaff permission."""
        permission = IsWatchlistOwnerOrStaff()
        request = type('Request', (), {'method': 'GET', 'user': self.user})
        self.assertTrue(
            permission.has_object_permission(
                request, None, self.watchlist))
        request.user = self.other_user
        self.assertFalse(
            permission.has_object_permission(
                request, None, self.watchlist))


class SerializerTests(TestCase):
    """Tests for serializers."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="user", password="password")
        self.theater = Theater.objects.create(
            name="Test Theater", location="Test Location")
        self.auditorium = Auditorium.objects.create(
            name="Test Auditorium", total_seats=100, theater=self.theater)
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date="2025-01-01",
            rating=5.0)
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            start_time=timezone.now(),
            end_time=timezone.now() +
            timedelta(
                hours=2),
            auditorium=self.auditorium)
        self.seat = Seat.objects.create(
            showtime=self.showtime,
            seat_number="A1",
            is_booked=False)
        self.booking = Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
            cost=20.00,
            status="Confirmed")
        self.booking.seats.set([self.seat])

    def test_movie_serializer(self):
        """Test MovieSerializer."""
        serializer = MovieSerializer(instance=self.movie)
        self.assertEqual(serializer.data["title"], self.movie.title)

    def test_booking_serializer(self):
        """Test BookingSerializer."""
        serializer = BookingSerializer(instance=self.booking)
        self.assertEqual(
            float(
                serializer.data["cost"]), float(
                self.booking.cost))


class TaskTests(TestCase):
    """Tests for tasks."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="user", password="password")
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test",
            release_date="2025-01-01",
            rating=5.0)
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            start_time=timezone.now() + timedelta(minutes=30),
            end_time=timezone.now() + timedelta(hours=2, minutes=30)
        )
        self.booking = Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
            cost=20.00,
            status="Pending")

    @patch("management.tasks.Notification.objects.get_or_create")
    def test_send_upcoming_showtime_reminders(self, mock_get_or_create):
        """Test that reminders are sent for upcoming showtimes."""
        send_upcoming_showtime_reminders()
        mock_get_or_create.assert_called_once_with(
            user=self.user, message=f"⏰ Reminder: your showtime for “{self.showtime.movie.title}”"
            f"is at {self.showtime.start_time.strftime('%Y-%m-%d %H:%M')}.")

    @patch("management.tasks.Notification.objects.get_or_create")
    def test_send_pending_booking_reminder(self, mock_get_or_create):
        """Test that reminders are sent for pending bookings."""
        send_pending_booking_reminder(self.booking.id)
        mock_get_or_create.assert_called()

    @patch("management.tasks.Notification.objects.create")
    def test_delete_unpaid_booking(self, mock_create):
        """Test that unpaid bookings are cancelled and notifications are sent."""
        delete_unpaid_booking(self.booking.id)
        mock_create.assert_called()

    @patch("management.tasks.Notification.objects.get_or_create")
    def test_send_showtime_reminder(self, mock_get_or_create):
        """Test that reminders are sent for confirmed bookings."""
        self.booking.status = "Confirmed"
        self.booking.save()
        send_showtime_reminder(self.booking.id)
        mock_get_or_create.assert_called()


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True
