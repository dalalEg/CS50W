from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect
# Create your views here.
from rest_framework import viewsets
from django.utils import timezone
from datetime import datetime
from rest_framework.decorators import api_view, action,permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .permissions import IsAdminOrReadOnly, IsReviewOwnerOrReadOnly,IsAuthenticated, IsBookingOwnerOrStaff, IsNotificationOwnerOrStaff
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .serializers import( MovieSerializer, ShowtimeSerializer, SeatSerializer, 
                         GenreSerializer, ReviewSerializer, NotificationSerializer,
                         BookingSerializer, ActorSerializer, DirectorSerializer,
                         ProducerSerializer, PaymentSerializer, WatchlistSerializer,
                         RoleSerializer, TheaterSerializer,UserSerializer,AuditoriumSerializer)
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import (User, Movie, Genre,Seat,Showtime,Review, 
                     Notification,Booking,Actor,Director,Auditorium,Producer,Payment,watchlist,Role,Theater)

def index(request):
    return render(request, 'management/index.html')
   
@csrf_exempt
def login_view(request,user=None):
    if request.method == 'POST':
        # Extract username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'management/login.html', {
                'title': 'Login',
                'error': 'Username and password are required.'
            })
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or the index page
            if user.is_superuser:
                return HttpResponseRedirect(reverse("admin:index"))
            return  render(request, 'management/index.html', {
                'title': 'Home',
                'name': user.username,
            })
        else:
            return render(request, 'management/login.html', {
                'title': 'Login',
                'error': 'Invalid username or password.'
            })
    else:
        return render(request, 'management/login.html')
        
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def register(request):
    """Register a new user."""
    # If the request method is POST, attempt to register the user
    if request.method == "POST":
        #Extract username, email, and password from the request
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        # Ensure username, email, and password provided
        if not username or not password or not email or not confirmation:
            return render(request, "management/register.html", {
                "message": "All fields are required."
        })
      
        # check that the email is valid 
        if not email or '@' not in email or '.' not in email.split('@')[-1] :
            return render(request, "management/register.html", {
                "message": "Invalid email address."
            })
        # check that the username and mail and not already in use
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, "management/register.html", {
                "message": "Username or email already taken."
            })
        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "management/register.html", {
                "message": "Passwords must match."
            })
        try:        
        # Attempt to create new user
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "management/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index", args=(user.username,)))
    else:
        return render(request, "management/register.html")
    

#API views (login and register).
@api_view(['POST'])
def api_login(request):
    """API endpoint for user login."""
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful.'})
    else:
        return Response({'error': 'Invalid username or password.'}, status=401)

@api_view(['POST'])
def api_register(request):
    """API endpoint for user registration."""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    confirmation = request.data.get('confirmation')
    if not username or not email or not password or not confirmation:
        return Response({'error': 'All fields are required.'}, status=400)
    if password != confirmation:
        return Response({'error': 'Passwords must match.'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken.'}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already taken.'}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    return Response({'message': 'Registration successful.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """API endpoint for user logout."""
    logout(request)
    return Response({'message': 'Logout successful.'}, status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_user_profile(request):
    """API endpoint to get the authenticated user's profile."""
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

 #API views (generic class-based or viewsets).
class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet for managing genres."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

class ActorViewSet(viewsets.ModelViewSet):
    """ViewSet for managing actors."""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrReadOnly]

class DirectorViewSet(viewsets.ModelViewSet):
    """ViewSet for managing directors."""
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProducerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing producers."""
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = [IsAdminOrReadOnly]

class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing roles."""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrReadOnly]

class MovieViewSet(viewsets.ModelViewSet):
    """ViewSet for managing movies."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]
    @action(detail=False, methods=['get'], url_path='popular')
    def get_popular_movies(self, request):
        """Custom action to get popular movies."""
        popular_movies = Movie.objects.filter(rating__gte=4.0).order_by('-rating')[:10]
        serializer = self.get_serializer(popular_movies, many=True)
        return Response(serializer.data)



class SeatViewSet(viewsets.ModelViewSet):
    """ViewSet for managing seats."""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAdminOrReadOnly]
class TheaterViewSet(viewsets.ModelViewSet):
    """ViewSet for managing theaters."""
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsAdminOrReadOnly]

class AuditoriumViewSet(viewsets.ModelViewSet):
    """ViewSet for managing auditoriums."""
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer
    permission_classes = [IsAdminOrReadOnly]

class ShowtimeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing showtimes."""
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Showtime.objects.all()
        return Showtime.objects.filter(start_time__gte=timezone.now())

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly]

class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing notifications."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsNotificationOwnerOrStaff, IsAuthenticated]
    def perform_create(self, serializer):       
        serializer.save(user=self.request.user)  


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bookings."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsBookingOwnerOrStaff, IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
           return Booking.objects.all()
        return Booking.objects.filter(user=user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
