from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_active = models.BooleanField(default=True)  # Override to ensure user is active
    points = models.PositiveIntegerField(default=0)  # Add points field
    email_verified = models.BooleanField(default=False)  # Add email verification field
   
    def __str__(self):
        return self.username
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "points": self.points,
            "email_verified": self.email_verified,
        }

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    genre =models.ManyToManyField('Genre', related_name='movies', blank=True)  # Add genre field
    def __str__(self):
        return self.title
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "release_date": self.release_date.isoformat(),
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "genre": [genre.name for genre in self.genre.all()],
        }
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    

class Seat (models.Model):
    showtime = models.ForeignKey('Showtime', on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.showtime.movie.title} - Seat {self.seat_number}"
    
    def serialize(self):
        return {
            "id": self.id,
            "movie": self.showtime.movie.title,
            "seat_number": self.seat_number,
            "is_booked": self.is_booked,
        }
    


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)  # Add location field
    is_VIP = models.BooleanField(default=False)  # Add is_VIP field
    thD_available = models.BooleanField(default=False)  # Add 3D_available field
    parking_available = models.BooleanField(default=False)  # Add parking_available field
    language = models.CharField(max_length=50, default='English')  # Add language field
    def __str__(self):
        return f"{self.movie.title} - {self.start_time} to {self.end_time}"
    def serialize(self):
        return {
            "id": self.id,
            "movie": self.movie.title,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "location": self.location,
            "is_VIP": self.is_VIP,
            "thD_available": self.thD_available,
            "parking_available": self.parking_available,
            "language": self.language,
        }
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} Review"
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "movie": self.movie.title,
            "content": self.content,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
        }
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    showtime = models.ForeignKey('Showtime', on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.PositiveIntegerField(default=1)  # Add seats field
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} booked {self.showtime.movie.title} on {self.booking_date}"
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "movie": self.showtime.movie.title,
            "showtime": self.showtime.start_time.isoformat(),
            "booking_date": self.booking_date.isoformat(),
            "seats": self.seats,
            "created_at": self.created_at.isoformat(),
        }
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat(),
        }
    


    
