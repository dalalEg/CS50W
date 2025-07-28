from django.test import TestCase
from .models import Movie

class MovieModelTest(TestCase):

    def setUp(self):
        Movie.objects.create(title="Inception", description="A mind-bending thriller", release_date="2010-07-16", duration=148)

    def test_movie_creation(self):
        movie = Movie.objects.get(title="Inception")
        self.assertEqual(movie.description, "A mind-bending thriller")
        self.assertEqual(movie.release_date, "2010-07-16")
        self.assertEqual(movie.duration, 148)