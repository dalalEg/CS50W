from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_active = models.BooleanField(default=True)  # Override to ensure user is active
    points = models.PositiveIntegerField(default=0)  # Add points field
    email_verified = models.BooleanField(default=False)  # Add email verification field
   
    def __str__(self):
        return self.username

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    genre =models.ManyToManyField('Genre', related_name='movies', blank=True)  # Add genre field
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)  # Add poster field
    trailer = models.URLField(blank=True, null=True)  # Add trailer field
    director = models.ForeignKey('Director', on_delete=models.CASCADE, related_name='movies', blank=True, null=True)  # Add director field
    producer = models.ForeignKey('Producer', on_delete=models.CASCADE, related_name='movies', blank=True, null=True)
    actors = models.ManyToManyField('Actor', related_name='movies', blank=True)  # Add actors field
    
    def get_genres(self):
        return ", ".join([genre.name for genre in self.genre.all()]) if self.genre.exists() else "No genres"
    
    def __str__(self):
        return self.title
   
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Seat (models.Model):
    showtime = models.ForeignKey('Showtime', on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)  # Add price field
    def __str__(self):
        return f"{self.showtime.movie.title} - Seat {self.seat_number}"
    
  
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_VIP = models.BooleanField(default=False)  # Add is_VIP field
    thD_available = models.BooleanField(default=False)  # Add 3D_available field
    parking_available = models.BooleanField(default=False)  # Add parking_available field
    language = models.CharField(max_length=50, default='English')  # Add language field
    auditorium = models.ForeignKey('Auditorium', on_delete=models.CASCADE, related_name='showtimes', blank=True, null=True)  # Add auditorium field
    def __str__(self):
        return f"{self.movie.title} - {self.start_time} to {self.end_time}"
    
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} Review"
   

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    showtime = models.ForeignKey('Showtime', on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.PositiveIntegerField(default=1)  # Add seats field
    created_at = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add cost field
    def __str__(self):
        return f"{self.user.username} booked {self.showtime.movie.title} on {self.booking_date}"
    
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
   


    
class Actor(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class Director(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class Producer(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.amount} on {self.payment_date}"
    
class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlists")
    added_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} Watchlist"
    

class Role(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='roles')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='roles')
    character_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.actor.name} as {self.character_name} in {self.movie.title}"
    

class Auditorium(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField(default=0)
    theater= models.ForeignKey('Theater', on_delete=models.CASCADE, related_name='auditorium', blank=True, null=True)  # Add theater field
    def __str__(self):
        return f"{self.name} - {self.location} ({self.total_seats} seats)"
    
class Theater(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    auditoriums = models.ManyToManyField(Auditorium, related_name='theaters', blank=True)
    def __str__(self):
        return f"{self.name} - {self.location}"