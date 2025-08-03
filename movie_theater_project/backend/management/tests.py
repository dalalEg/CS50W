from email import contentmanager
from venv import create
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .views import MovieViewSet, ShowtimeViewSet, GenreViewSet, ActorViewSet, DirectorViewSet, ProducerViewSet, RoleViewSet, TheaterViewSet, AuditoriumViewSet, ReviewViewSet, NotificationViewSet, SeatViewSet, BookingViewSet
from .models import Movie, Showtime, Genre, Actor, Director, Producer, Role, Theater, Auditorium, Review, Notification, Seat, Booking
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
 
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
            username="user", password="userpass"
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
        # FIXED: Use the correct field name "character_name" instead of "name"
        self.role = Role.objects.create(character_name="Lead Actor", actor=self.actor, movie=self.movie)
        
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
            is_booked=True
        )
        self.booking = Booking.objects.create(
            user=self.regular_user,
            showtime=self.showtime,
            booking_date=self.showtime.start_time,
            # FIXED: Use the correct field name "cost" instead of "seat"
            cost=20.00,  # Assuming a fixed cost for simplicity
            # FIXED: Use the correct field name "seats" instead of "seat"
            seats=2,
            created_at=timezone.now()
        )
        self.movie.genre.add(self.genre)  # many-to-many relationship
        self.movie.actors.add(self.actor)
        
        # API client for requests
        self.client = APIClient()

    def login_as_admin(self):
        """Utility method to log in as an admin user."""
        self.client.login(username="admin", password="adminpass")

    def login_as_user(self):
        """Utility method to log in as a regular user."""
        self.client.login(username="user", password="userpass")

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
        self.assertEqual(Genre.objects.get(id=response.data['id']).name, 'Action')

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
        response = self.client.put(f'/api/genres/{self.genre.id}/', {'name': 'Sci-Fi'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, 'Sci-Fi')
    def test_update_genre_as_user(self):
        """Test updating a genre as a regular user."""
        """Regular users should not be able to update genres."""
        self.login_as_user()
        response = self.client.put(f'/api/genres/{self.genre.id}/', {'name': 'Sci-Fi'})
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
        self.assertEqual(Actor.objects.get(id=response.data['id']).name, 'Tom Hardy')
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

class DirectorAPITests(BaseAPITestCase):
    """Tests for the Director API endpoints.
    """
    def test_create_director_as_admin(self):
        """Test creating a director as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/directors/', {
            'name': 'Steven Spielberg',
            'biography': 'An American film director, producer, and screenwriter.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Director.objects.count(), 2)
        self.assertEqual(Director.objects.get(id=response.data['id']).name, 'Steven Spielberg')
    def test_create_director_as_user(self):
        """Test creating a director as a regular user."""
        self.login_as_user()    
        response = self.client.post('/api/directors/', {
            'name': 'Steven Spielberg',
            'biography': 'An American film director, producer, and screenwriter.'
        })
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


class ProducerAPITests(BaseAPITestCase):    
    """Tests for the Producer API endpoints.
    """
    def test_create_producer_as_admin(self):
        """Test creating a producer as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/producers/', {
            'name': 'Kathleen Kennedy',
            'biography': 'An American film producer and president of Lucasfilm.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producer.objects.count(), 2)
        self.assertEqual(Producer.objects.get(id=response.data['id']).name, 'Kathleen Kennedy')

    def test_create_producer_as_user(self): 
        """Test creating a producer as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/producers/', {
            'name': 'Kathleen Kennedy',
            'biography': 'An American film producer and president of Lucasfilm.'
        })
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

class RoleAPITests(BaseAPITestCase):
    """Tests for the Role API endpoints.
    """
    def test_create_role_as_admin(self):
        """Test creating a role as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/roles/', {
            'character_name': 'Protagonist',
            'actor': self.actor.id,
            'movie': self.movie.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 2)
        self.assertEqual(Role.objects.get(id=response.data['id']).character_name, 'Protagonist')
    def test_create_role_as_user(self):
        """Test creating a role as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/roles/', {
            'character_name': 'Protagonist',
            'actor': self.actor.id,
            'movie': self.movie.id
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
        self.assertEqual(response.data['character_name'], self.role.character_name)
    def test_update_role_as_admin(self):
        """Test updating a role as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/roles/{self.role.id}/', {
            'character_name': 'Main Character',
            'actor': self.actor.id, 
            'movie': self.movie.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.character_name, 'Main Character')    
    def test_update_role_as_user(self):
        """Test updating a role as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/roles/{self.role.id}/', {
            'character_name': 'Main Character',
            'actor': self.actor.id,
            'movie': self.movie.id
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
        response = self.client.post('/api/movies/', {
            'title': 'The Matrix',
            'description': 'A hacker discovers the reality is a simulation.',
            'release_date': '2024-02-01',
            'rating': 8.7,
            'director': self.director.id,
            'producer': self.producer.id,
            'genre': [self.genre.id],
            'actors': [self.actor.id],
            'poster': '',  # Assuming poster is optional for this test
            'trailer': ''  # Assuming trailer is optional for this test

        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(Movie.objects.get(id=response.data['id']).title, 'The Matrix')
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
        self.assertEqual(len(response.data), 1) # Only the initial movie should be present
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
        self.assertEqual(Movie.objects.count(), 0)
    def test_delete_movie_as_user(self):
        self.login_as_user()
        response = self.client.delete(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Movie.objects.count(), 1)
    def test_movie_serializer_fields(self):
        self.login_as_admin()
        response = self.client.get(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = [
            'id', 'title', 'description', 'release_date',
            'rating', 'created_at', 'poster', 'trailer',
            'director', 'actors', 'producer', 'genre'
        ]
        self.assertEqual(set(response.data.keys()), set(expected_fields))
    
    def test_popular_movies_action(self):
        """Test the custom action to get popular movies."""
        self.login_as_admin()
        response = self.client.get('/api/movies/popular/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        for movie in response.data:
            self.assertGreaterEqual(movie['rating'], 4.0)


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
        self.assertEqual(Theater.objects.get(id=response.data['id']).name, 'Downtown Cinema')
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
        self.assertEqual(Auditorium.objects.get(id=response.data['id']).name, 'Auditorium 2')
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
        response = self.client.delete(f'/api/auditoriums/{self.auditorium.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Auditorium.objects.count(), 0)     

    def test_delete_auditorium_as_user(self):
        """Test deleting an auditorium as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/auditoriums/{self.auditorium.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Auditorium.objects.count(), 1)

class ShowtimeAPITests(BaseAPITestCase):
    """Tests for the Showtime API endpoints.
    """
    def test_create_showtime_as_admin(self):
        """Test creating a showtime as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/showtimes/', {
            'movie': self.movie.id,
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
        self.assertEqual(Showtime.objects.get(id=response.data['id']).movie.title, 'Inception')

    def test_create_showtime_as_user(self):
        """Test creating a showtime as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/showtimes/', {
            'movie': self.movie.id,
            'start_time': timezone.now() + timedelta(days=2),
            'end_time': timezone.now() + timedelta(days=2, hours=2),
            'auditorium': self.auditorium.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_list_showtimes(self):
        """Test listing all showtimes."""
        response = self.client.get('/api/showtimes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['movie']['title'], 'Inception')
    def test_retrieve_showtime(self):
        """Test retrieving a specific showtime."""
        response = self.client.get(f'/api/showtimes/{self.showtime.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['movie']['title'], 'Inception')
    def test_update_showtime_as_admin(self):
        """Test updating a showtime as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/showtimes/{self.showtime.id}/', {
            'movie': self.movie.id, 
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
        self.assertAlmostEqual(self.showtime.start_time.timestamp(), 
                               (timezone.now() + timedelta(days=3)).timestamp(), delta=5)
        self.assertAlmostEqual(self.showtime.end_time.timestamp(), 
                               (timezone.now() + timedelta(days=3, hours=2)).timestamp(), delta=5)
    def test_update_showtime_as_user(self):
        """Test updating a showtime as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/showtimes/{self.showtime.id}/', {
            'movie': self.movie.id,
            'start_time': timezone.now() + timedelta(days=3),
            'end_time': timezone.now() + timedelta(days=3, hours=2),    
            'auditorium': self.auditorium.id
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
        self.assertEqual(Showtime.objects.get(id=self.showtime.id).movie.title, 'Inception')

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
        self.assertEqual(Seat.objects.get(id=response.data['id']).seat_number, 'A1')
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
            'movie': self.movie.id,
            'rating': 5,
            'content': 'Great movie!'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get(id=response.data['id']).content, 'Great movie!')
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
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    def test_retrieve_review(self):
        """Test retrieving a specific review."""
        # First create a review to retrieve
        self.login_as_user()
        self.client.post('/api/reviews/', {
            'movie': self.movie.id,
            'rating': 5,
            'content': 'Great movie!'
        })
        response = self.client.get(f'/api/reviews/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['movie'], self.movie.id)
    def test_update_review_as_user(self):
        """Test updating a review as a regular user."""
        self.login_as_user()
        # First create a review to update
        self.client.post('/api/reviews/', {
            'movie': self.movie.id,
            'rating': 5,
            'content': 'Great movie!'
        })
        review = Review.objects.first()
        response = self.client.put(f'/api/reviews/{review.id}/', {
            'movie': self.movie.id,
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
        self.assertEqual(Review.objects.count(), 1)  # Review should still exist



class BookingAPITests(BaseAPITestCase):
    """Tests for the Booking API endpoints.
    """
    def test_create_booking_as_user(self):
        """Test creating a booking as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime': self.showtime.id,
            'seats': 2,
            'booking_date': timezone.now().isoformat(),
            'cost': 20.00,  # Assuming a fixed cost for simplicity
            'created_at': timezone.now().isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(Booking.objects.get(id=response.data['id']).seats, 2)
    def test_create_booking_as_anonymous(self): 
        """Test creating a booking as an anonymous user."""
        response = self.client.post('/api/bookings/', {
            'showtime': self.showtime.id,
            'seats': 2,
            'booking_date': timezone.now().isoformat(),
            'cost': 20.00,
            'created_at': timezone.now().isoformat()
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
            'showtime': self.showtime.id,
            'seats': 2,
            'booking_date': timezone.now().isoformat(),
            'cost': 20.00,
            'created_at': timezone.now().isoformat()
        })
        booking_id = response.data['id']
        response = self.client.get(f'/api/bookings/{booking_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], booking_id)
    def test_update_booking_as_user(self):
        """Test updating a booking as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime': self.showtime.id,
            'seats': 2,
            'booking_date': timezone.now().isoformat(),
            'cost': 20.00,
            'created_at': timezone.now().isoformat()
        })
        booking_id = response.data['id']
        response = self.client.put(f'/api/bookings/{booking_id}/', {
            'showtime': self.showtime.id,
            'seats': 3,
            'booking_date': timezone.now().isoformat(),
            'cost': 30.00,
            'created_at': timezone.now().isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['seats'], 3)
        self.assertEqual(float(response.data['cost']), 30.00)
    def test_update_booking_as_anonymous(self):
        """Test updating a booking as an anonymous user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime': self.showtime.id,
            'seats': 2,
            'booking_date': timezone.now().isoformat(),
            'cost': 20.00,
            'created_at': timezone.now().isoformat()
        })
        booking_id = response.data['id']
        self.client.logout()
        response = self.client.put(f'/api/bookings/{booking_id}/', {
            'showtime': self.showtime.id,
            'seats': 3,
            'booking_date': timezone.now().isoformat(),
            'cost': 30.00,
            'created_at': timezone.now().isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_delete_booking_as_user(self):
        """Test deleting a booking as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime': self.showtime.id,
            'seats': 2,
            'booking_date': timezone.now().isoformat(),
            'cost': 20.00,
            'created_at': timezone.now().isoformat()
        })
        booking_id = response.data['id']
        response = self.client.delete(f'/api/bookings/{booking_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 1)
    def test_delete_booking_as_anonymous(self):
        """Test deleting a booking as an anonymous user."""
        self.login_as_user()
        response = self.client.post('/api/bookings/', {
            'showtime': self.showtime.id,
            'seats': 2,
            'booking_date': timezone.now().isoformat(),
            'cost': 20.00,
            'created_at': timezone.now().isoformat()
        })
        booking_id = response.data['id']
        self.client.logout()
        response = self.client.delete(f'/api/bookings/{booking_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Booking.objects.count(), 2)  # Booking should still exist


class NotificationAPITests(BaseAPITestCase):
    """Tests for the Notification API endpoints.
    """
    def test_create_notification_as_admin(self):
        """Test creating a notification as an admin user."""
        self.login_as_admin()
        response = self.client.post('/api/notifications/', {
            'message': 'New movie released!',
            'created_at': timezone.now().isoformat(),
            'is_read': False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(Notification.objects.get(id=response.data['id']).message, 'New movie released!')
    def test_create_notification_as_user(self):
        """Test creating a notification as a regular user."""
        self.login_as_user()
        response = self.client.post('/api/notifications/',
            {
                'message': 'New movie released!',   
                'created_at': timezone.now().isoformat(),
                'is_read': False
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_list_notifications(self):
        """Test listing all notifications."""
        self.login_as_user()
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'New movie added: Inception')
        self.assertEqual(response.data[0]['is_read'], False)

    def test_retrieve_notification(self):
        """Test retrieving a specific notification."""
        self.login_as_user()
        response = self.client.get(f'/api/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.notification.message)
    def test_update_notification_as_admin(self):    
        """Test updating a notification as an admin user."""
        self.login_as_admin()
        response = self.client.put(f'/api/notifications/{self.notification.id}/', {
            'message': 'Updated notification message',  
            'created_at': timezone.now().isoformat(),
            'is_read': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)      
        self.notification.refresh_from_db()
        self.assertEqual(self.notification.message, 'Updated notification message')
        self.assertTrue(self.notification.is_read)
    def test_update_notification_as_user(self): 
        """Test updating a notification as a regular user."""
        self.login_as_user()
        response = self.client.put(f'/api/notifications/{self.notification.id}/', {
            'message': 'Updated notification message',
            'created_at': timezone.now().isoformat(),
            'is_read': True
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_delete_notification_as_admin(self):
        """Test deleting a notification as an admin user."""
        self.login_as_admin()
        response = self.client.delete(f'/api/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Notification.objects.count(), 0)
    def test_delete_notification_as_user(self):
        """Test deleting a notification as a regular user."""
        self.login_as_user()
        response = self.client.delete(f'/api/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Notification.objects.count(), 1)   
        self.assertEqual(Notification.objects.get(id=self.notification.id).message, 'New movie added: Inception') 
