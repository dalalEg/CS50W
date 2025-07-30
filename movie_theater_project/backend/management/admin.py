from django.contrib import admin
from .models import User, Movie, Genre, Seat, Review,Showtime,Booking,Notification

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating')
    search_fields = ('title',)
    list_filter = ('release_date', 'rating')    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('genre')
    

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('movies')
    

class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'is_booked', 'Showtime')  # 'Showtime' should match the model field name
    # If you want to show the movie title, you can add a method:
    def movie_title(self, obj):
        return obj.Showtime.movie.title
    movie_title.short_description = 'Movie'
    list_display = ('seat_number', 'is_booked', 'Showtime', 'movie_title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('rating', 'created_at')
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'movie')    
    

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'start_time','end_time', 'location')
    search_fields = ('movie__title', 'location')
    list_filter = ('start_time', 'end_time', 'location')
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('movie').prefetch_related('seats') 
    


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'showtime', 'created_at')
    search_fields = ('user__username', 'showtime__movie__title')
    list_filter = ('created_at',)
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'showtime')
    


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):  
    list_display = ('user', 'message', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('created_at',)
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')