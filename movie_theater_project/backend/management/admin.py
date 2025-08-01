from django.contrib import admin
from .models import (
    User, Movie, Genre, Seat, Review, Showtime, Booking, Notification,
    Actor, Director, Producer, Payment, watchlist, Role, Auditorium, Theater
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'points', 'email_verified')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'email_verified')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating')
    search_fields = ('title',)
    list_filter = ('release_date', 'rating', 'genre')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'is_booked', 'showtime', 'price')
    list_filter = ('is_booked', 'showtime')
    search_fields = ('seat_number',)

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'start_time', 'end_time', 'is_VIP', 'thD_available', 'parking_available', 'language', 'auditorium')
    list_filter = ('is_VIP', 'thD_available', 'parking_available', 'language', 'auditorium')
    search_fields = ('movie__title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('rating', 'created_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'showtime', 'booking_date', 'seats', 'cost')
    search_fields = ('user__username', 'showtime__movie__title')
    list_filter = ('booking_date',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('is_read', 'created_at')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    search_fields = ('name',)

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    search_fields = ('name',)

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    search_fields = ('name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('user__username',)

@admin.register(watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'added_at')
    search_fields = ('user__username', 'movie__title')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('actor', 'movie', 'character_name')
    search_fields = ('actor__name', 'movie__title', 'character_name')

@admin.register(Auditorium)
class AuditoriumAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_seats', 'available_seats', 'theater')
    search_fields = ('name', 'theater__name')

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')