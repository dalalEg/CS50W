from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from . import views 

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
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
router.register(r'watchlist', views.WatchlistViewSet)  
router.register(r'rate-services', views.RateServiceViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'favorites', views.FavouriteViewSet)

# Add other viewsets as needed
urlpatterns = [
    path('', views.index, name='index'),
    # Add other URL patterns here as needed
    path ('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('api/confirm/<int:uid>/<str:token>/', views.confirm_email, name='confirm-email'),
    path('api/auth/generate_token/', views.generate_token, name='generate-confirmation-token'),
    path('api/auth/login/',   views.api_login,        name='api-login'),
    path('api/auth/logout/',  views.api_logout,       name='api-logout'),
    path('api/auth/user/',    views.api_user_profile, name='api-current-user'),
    path('api/auth/register/', views.api_register, name='api-register'),
    path('api/', include(router.urls)),  # Include the API URLs

]


