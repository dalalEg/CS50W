from rest_framework import serializers
from .models import (
    User, Movie, Booking, Showtime, Seat,
    Genre, Review, Notification, Actor, Director,Producer, Payment,
    watchlist, Role, Auditorium, Theater
)
from rest_framework.validators import UniqueValidator
from django.db import transaction
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Corrected from 'all'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class ActorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
      validators=[UniqueValidator(queryset=Actor.objects.all())]
    )
    class Meta:
        model = Actor
        fields = ['id','name','date_of_birth','biography']

class DirectorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
      validators=[UniqueValidator(queryset=Director.objects.all())]
    )
    class Meta:
        model = Director
        fields = ['id','name','date_of_birth','biography']

class ProducerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
      validators=[UniqueValidator(queryset=Producer.objects.all())]
    )
    class Meta:
        model = Producer
        fields = ['id','name','date_of_birth','biography']

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
    theater = TheaterSerializer(read_only=True)  # for reading
    class Meta:
        model = Auditorium
        fields = ['id', 'name', 'theater', 'total_seats', 'available_seats']

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
    seat_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model  = Booking
        fields = ['id','showtime','seat_ids','seats','cost','created_at']
        read_only_fields = ['seats','cost']

    def create(self, validated_data):
        ids   = validated_data.pop('seat_ids')
        seats = list(Seat.objects.filter(id__in=ids))
        total = sum(s.price for s in seats)
        # create the booking with both count and cost
        booking = Booking.objects.create(
            **validated_data,
            seats=len(seats),
            cost=total
        )
        # mark them booked
        Seat.objects.filter(id__in=ids).update(is_booked=True)
        return booking

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

