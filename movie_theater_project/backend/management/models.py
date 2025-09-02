from django.contrib.auth.models import AbstractUser
from django.db import models
from celery import shared_task

# Create your models here.


class User(AbstractUser):
    # Override to ensure user is active
    is_active = models.BooleanField(default=True)
    points = models.PositiveIntegerField(default=0)  # Add points field
    email_verified = models.BooleanField(
        default=False)  # Add email verification field

    def __str__(self):
        return self.username


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    genre = models.ManyToManyField(
        'Genre',
        related_name='movies',
        blank=True)  # Add genre field
    poster = models.ImageField(
        upload_to='posters/',
        blank=True,
        null=True)  # Add poster field
    trailer = models.URLField(blank=True, null=True)  # Add trailer field
    director = models.ForeignKey(
        'Director',
        on_delete=models.CASCADE,
        related_name='movies',
        blank=True,
        null=True)  # Add director field
    producer = models.ForeignKey(
        'Producer',
        on_delete=models.CASCADE,
        related_name='movies',
        blank=True,
        null=True)
    actors = models.ManyToManyField(
        'Actor',
        related_name='movies',
        blank=True)  # Add actors field
    duration = models.DurationField(
        blank=True, null=True)  # Add duration field

    def get_genres(self):
        return ", ".join([genre.name for genre in self.genre.all()]
                         ) if self.genre.exists() else "No genres"

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Seat (models.Model):
    showtime = models.ForeignKey(
        'Showtime',
        on_delete=models.CASCADE,
        related_name="seats")
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=10.00)  # Add price field

    def __str__(self):
        return f"{self.showtime.movie.title} - Seat {self.seat_number}"


class Showtime(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="showtimes")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_VIP = models.BooleanField(default=False)  # Add is_VIP field
    thD_available = models.BooleanField(
        default=False)  # Add 3D_available field
    parking_available = models.BooleanField(
        default=False)  # Add parking_available field
    language = models.CharField(max_length=50,
                                default='English')  # Add language field
    auditorium = models.ForeignKey(
        'Auditorium',
        on_delete=models.CASCADE,
        related_name='showtimes',
        blank=True,
        null=True)  # Add auditorium field
    available_seats = models.PositiveIntegerField(
        default=0)  # Add available_seats field

    def save(self, *args, **kwargs):
        # only seed available_seats on first create
        if self._state.adding and self.auditorium:
            self.available_seats = self.auditorium.total_seats
        super().save(*args, **kwargs)

    def __str__(self):
        start = self.start_time.strftime("%Y-%m-%d %H:%M:%S")
        end = self.end_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.movie.title} - {start} to {end}"


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews")
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews")
    content = models.TextField()
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} Review"


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings")
    showtime = models.ForeignKey(
        'Showtime',
        on_delete=models.CASCADE,
        related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.ManyToManyField('Seat', related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00)  # Add cost field
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending',
             'Pending'),
            ('Confirmed',
             'Confirmed'),
            ('Cancelled',
             'Cancelled')],
        default='Pending')  # Add status field
    attended = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.user.username} booked "
            f"{self.showtime.movie.title} on "
            f"{self.booking_date}"
        )


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ( f"Notification for {self.user.username}:"
                 f"{self.message}"
        )

class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments")
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments",
        blank=True,
        null=True)  # Add booking field
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('Credit Card',
             'Credit Card'),
            ('Debit Card',
             'Debit Card'),
            ('PayPal',
             'PayPal')],
        default='Credit Card')
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending',
             'Pending'),
            ('Completed',
             'Completed'),
            ('Failed',
             'Failed')],
        default='Pending')
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True)  # Add created_at field

    def __str__(self):
        return (f"Payment {self.pk} for Booking"
                f" {self.booking_id}: {self.status}")



class watchlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlists")
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="watchlists")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} Watchlist"


class Role(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        related_name='roles')
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='roles')
    character_name = models.CharField(max_length=100)

    def __str__(self):
        return (f"{self.actor.name} as"
                f"{self.character_name} in {self.movie.title}")


class Auditorium(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField(default=0)
    theater = models.ForeignKey(
        'Theater',
        on_delete=models.CASCADE,
        related_name='auditorium',
        blank=True,
        null=True)  # Add theater field

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.theater.location} "
            f"({self.total_seats} seats)"
        )


class Theater(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.location}"


class RateService(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rate_services")
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="rate_services",
        blank=True,
        null=True)  # Add booking field
    all_rating = models.PositiveIntegerField(
        default=0, choices=[
            (i, str(i)) for i in range(
                1, 6)])  # Add all_rating field with choices
    show_rating = models.PositiveIntegerField(
        default=0, choices=[
            (i, str(i)) for i in range(
                1, 6)])  # Add show_rating field with choices
    auditorium_rating = models.PositiveIntegerField(
        default=0, choices=[
            (i, str(i)) for i in range(
                1, 6)])  # Add auditorium_rating field with choices
    comment = models.TextField(blank=True, null=True)  # Add comment field

    def __str__(self):
        movie = (
            self.booking.showtime.movie.title
            if self.booking and self.booking.showtime
            else "Unknown"
        )
        return f"Service Review by {self.user.username} for {movie}"


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favourites")
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="favourites")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} Favourite"
