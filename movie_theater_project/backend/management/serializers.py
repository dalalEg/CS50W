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
        fields = ['id', 'name', 'biography']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name', 'biography']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name', 'biography', ]

class MovieSerializer(serializers.ModelSerializer):
    genre_list = serializers.SerializerMethodField()
    director = DirectorSerializer(read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    producer = ProducerSerializer(read_only=True)
    poster = serializers.ImageField(use_url=True, required=False)
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date',
            'genre_list', 'rating', 'created_at', 'poster',
            'trailer', 'director', 'actors','producer'
        ]
    def get_genre_list(self, obj):
        return obj.get_genres()
class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ['id', 'name', 'location']

class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = ['id', 'name', 'theater', 'total_seats']

class ShowtimeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    auditorium = AuditoriumSerializer(read_only=True)  # for reading

    # To allow POST/PUT, use a writable field as well:
    auditorium_id = serializers.PrimaryKeyRelatedField(
        source='auditorium', queryset=Auditorium.objects.all(), write_only=True
    )

    class Meta:
        model = Showtime
        fields = [
            'id', 'movie', 'start_time', 'end_time',
            'parking_available', 'thD_available', 'language',
            'is_VIP', 'auditorium', 'auditorium_id'
        ]

class SeatSerializer(serializers.ModelSerializer):
    showtime = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all())

    class Meta:
        model = Seat
        fields = ['id', 'showtime', 'seat_number', 'is_booked', 'price']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'content', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    showtime = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all())
  
    class Meta:
        model = Booking
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},  # user is set in view
        }


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
    actor = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    class Meta:
        model = Role
        fields = ['id', 'character_name', 'actor', 'movie']

