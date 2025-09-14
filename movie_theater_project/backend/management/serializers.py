from rest_framework import serializers
from .models import (
    User, Movie, Booking, Showtime, Seat,
    Genre, Review, Notification, Actor, Director, Producer, Payment,
    watchlist, Role, Auditorium, Theater, RateService, Favourite, News
)
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault


class UserSerializer(serializers.ModelSerializer):
    email_verified = serializers.BooleanField(read_only=True)

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
        fields = ['id', 'name', 'date_of_birth', 'biography']


class DirectorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Director.objects.all())]
    )

    class Meta:
        model = Director
        fields = ['id', 'name', 'date_of_birth', 'biography']


class ProducerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Producer.objects.all())]
    )

    class Meta:
        model = Producer
        fields = ['id', 'name', 'date_of_birth', 'biography']


class MovieSerializer(serializers.ModelSerializer):
    # ── READ-ONLY NESTED OUTPUT ────────────────────────────
    genres = GenreSerializer(source='genre', many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    producer = ProducerSerializer(read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    poster = serializers.ImageField(use_url=True, required=False)
    duration = serializers.DurationField(required=False)

    # ── WRITE-ONLY PK INPUT ────────────────────────────────
    director_id = serializers.PrimaryKeyRelatedField(
        queryset=Director.objects.all(),
        source="director",
        write_only=True,
        required=False
    )
    producer_id = serializers.PrimaryKeyRelatedField(
        queryset=Producer.objects.all(),
        source="producer",
        write_only=True,
        required=False
    )
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source="genre",
        many=True,
        write_only=True,
        required=False
    )
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        source="actors",
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Movie
        fields = [
            "id", "title", "description", "release_date", "rating",
            "poster", "trailer", "duration", "created_at",
            # read-only expanded
            "genres", "director", "producer", "actors",
            # write-only IDs
            "director_id", "producer_id", "genre_ids", "actor_ids",
        ]

    def get_genres(self):
        return ", ".join([genre.name for genre in self.genre.all()]
                         ) if self.genre.exists() else "No genres"


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
    auditorium = AuditoriumSerializer(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    auditorium_id = serializers.PrimaryKeyRelatedField(
        source='auditorium',
        queryset=Auditorium.objects.all(),
        write_only=True
    )
    movie_id = serializers.PrimaryKeyRelatedField(
        source='movie',
        queryset=Movie.objects.all(),
        write_only=True
    )

    class Meta:
        model = Showtime
        fields = [
            'id',
            'movie',
            'start_time',
            'end_time',
            'available_seats',    # ← add this
            'parking_available',
            'thD_available',
            'language',
            'is_VIP',
            'auditorium',
            'auditorium_id',
            'movie_id'
        ]


class SeatSerializer(serializers.ModelSerializer):
    showtime = serializers.PrimaryKeyRelatedField(
        queryset=Showtime.objects.all())

    class Meta:
        model = Seat
        fields = ['id', 'showtime', 'seat_number', 'is_booked', 'price']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    content = serializers.CharField(
        max_length=1000,
        allow_blank=False
    )
    rating = serializers.IntegerField(
        required=True,
        min_value=1,
        max_value=5
    )
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',  # maps to the `movie` FK
        write_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'movie',
            'content',
            'rating',
            'created_at',
            'updated_at',
            'anonymous',
            'movie_id']
        read_only_fields = ['id', 'user', 'movie', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    # output fields
    showtime = ShowtimeSerializer(read_only=True)
    seats = SeatSerializer(many=True, read_only=True)
    attended = serializers.BooleanField(read_only=True)
    # input‐only fields
    showtime_id = serializers.PrimaryKeyRelatedField(
        queryset=Showtime.objects.all(),
        source='showtime',
        write_only=True
    )
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'showtime',     # nested read‐only
            'showtime_id',  # write‐only
            'seats',        # read‐only
            'seat_ids',     # write‐only
            'cost',
            'created_at',
            'status',
            'attended',
        ]
        read_only_fields = ['cost', 'status', 'attended']

    def create(self, validated_data):
        user = validated_data.pop('user')
        # now present thanks to source='showtime'
        showtime = validated_data.pop('showtime')
        seat_ids = validated_data.pop('seat_ids')
        seats_qs = Seat.objects.filter(id__in=seat_ids, is_booked=False)
        seats = list(seats_qs)
        if len(seats) != len(seat_ids):
            raise ValidationError("One or more seats are already booked.")

        total = sum(s.price for s in seats)

        with transaction.atomic():
            updated = Showtime.objects.filter(
                id=showtime.id,
                available_seats__gte=len(seats)
            ).update(
                available_seats=F('available_seats') - len(seats)
            )
            if not updated:
                raise ValidationError("Not enough seats available.")

            booking = Booking.objects.create(
                user=user,
                showtime=showtime,
                cost=total
            )
            booking.seats.set(seats)
            seats_qs.update(is_booked=True)

        return booking

    def update(self, instance, validated_data):
        seat_ids = validated_data.pop('seat_ids', None)
        if seat_ids is not None:
            with transaction.atomic():
                # release seats the user unchecked
                to_release = instance.seats.exclude(id__in=seat_ids)
                released_count = to_release.count()
                to_release.update(is_booked=False)
                Showtime.objects.filter(pk=instance.showtime_id).update(
                    available_seats=F('available_seats') + released_count
                )

                # finally update the M2M and recalc cost
                instance.seats.set(seat_ids)
                instance.cost = sum(s.price for s in instance.seats.all())
                instance.save()
        return instance


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'message', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Notification.objects.create(user=user, **validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    booking_id = serializers.PrimaryKeyRelatedField(
        source='booking',
        queryset=Booking.objects.all(),
        write_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'booking',
            'amount',
            'status',
            'created_at',
            'payment_method',
            'payment_date',
            'booking_id']
        read_only_fields = ['id', 'status', 'created_at']


class WatchlistSerializer(serializers.ModelSerializer):
    # Automatically assign the logged-in user; do not expect it in the payload
    user = serializers.HiddenField(default=CurrentUserDefault())

    # If you still want to return full user data, add a separate read‐only
    # field:
    user_info = UserSerializer(source='user', read_only=True)

    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        source='movie',
        queryset=Movie.objects.all(),
        write_only=True
    )

    class Meta:
        model = watchlist
        fields = ['id', 'user', 'user_info', 'movie', 'movie_id', 'added_at']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=watchlist.objects.all(),
                fields=['user', 'movie'],
                message="This movie is already in your watchlist."
            )
        ]


class RoleSerializer(serializers.ModelSerializer):
    # IDs for input
    actor_id = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(), source="actor", write_only=True
    )
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source="movie", write_only=True
    )

    # Nested serializers for output
    actor = ActorSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Role
        fields = [
            "id",
            "actor",
            "movie",
            "character_name",
            "actor_id",
            "movie_id"]


class RateServiceSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=CurrentUserDefault())
    booking = serializers.PrimaryKeyRelatedField(read_only=True)
    booking_id = serializers.PrimaryKeyRelatedField(
        source='booking',
        queryset=Booking.objects.all(),      # allow any booking
        write_only=True
    )

    class Meta:
        model = RateService
        fields = ['id', 'user', 'booking', 'booking_id',
                  'all_rating', 'show_rating', 'auditorium_rating', 'comment']

        validators = [
            UniqueTogetherValidator(
                queryset=RateService.objects.all(),
                fields=['user', 'booking'],
                message="You've already submitted a service review for this booking."
            )
        ]


class FavouriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Favourite
        fields = ['id', 'user', 'movie', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'published_at']
