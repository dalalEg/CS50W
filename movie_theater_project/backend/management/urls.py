from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views 

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'showtimes', views.ShowtimeViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'actors', views.ActorViewSet)
router.register(r'directors', views.DirectorViewSet)    
router.register(r'producers', views.ProducerViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'theaters', views.TheaterViewSet)
router.register(r'auditoriums', views.AuditoriumViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet)
# Add other viewsets as needed
urlpatterns = [
    path('', views.index, name='index'),
    # Add other URL patterns here as needed
    path ('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('api/', include(router.urls)),  # Include the API URLs

]


