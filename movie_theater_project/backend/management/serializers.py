from rest_framework import serializers
from .models import (
    User, Movie, Booking, Showtime, Seat,
    Genre, Review, Notification, Actor, Director,Producer, Payment,
    watchlist, Role, Auditorium, Theater
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Corrected from 'all'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'bio', 'photo']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name', 'bio', 'photo']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name', 'bio', 'photo']

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    producer = ProducerSerializer(read_only=True)
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date',
            'genre', 'rating', 'created_at', 'poster',
            'trailer', 'director', 'actors','producer'
        ]

class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ['id', 'name', 'location']

class AuditoriumSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer(read_only=True)
    class Meta:
        model = Auditorium
        fields = ['id', 'name', 'theater', 'capacity']
class ShowtimeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    auditorium = AuditoriumSerializer(read_only=True)
    class Meta:
        model = Showtime
        fields = [
            'id', 'movie', 'start_time', 'end_time',
            'location', 'is_VIP', 'thD_available',
            'parking_available', 'language'
        ]


class SeatSerializer(serializers.ModelSerializer):
    showtime = ShowtimeSerializer(read_only=True)

    class Meta:
        model = Seat
        fields = ['id', 'showtime', 'seat_number', 'is_booked', 'price']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'content', 'created_at', 'cost']


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    showtime = ShowtimeSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'showtime', 'seats', 'booking_date', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'payment_date']


class WatchlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True) 

    class Meta:
        model = watchlist
        fields = ['id', 'user', 'movie', 'added_at']

class RoleSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Role
        fields = ['id', 'actor', 'movie', 'character_name']

