from ast import Is
from encodings import search_function
from re import search
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect
from rest_framework import viewsets,filters,generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import datetime
from rest_framework.decorators import api_view,action,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .permissions import IsAdminOrReadOnly, IsReviewOwnerOrReadOnly,IsAuthenticated, IsBookingOwnerOrStaff, IsNotificationOwnerOrStaff
from .permissions import IsWatchlistOwnerOrStaff
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .serializers import( MovieSerializer, ShowtimeSerializer, SeatSerializer, 
                         GenreSerializer, ReviewSerializer, NotificationSerializer,
                         BookingSerializer, ActorSerializer, DirectorSerializer,
                         ProducerSerializer, PaymentSerializer, WatchlistSerializer,
                         RoleSerializer, TheaterSerializer,UserSerializer,AuditoriumSerializer,
                         RateServiceSerializer)
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator
from rest_framework import status
from django.db import transaction
from django.db.models import F
from django.contrib.auth.models import User
from rest_framework import routers  
from .models import (User, Movie, Genre,Seat,Showtime,Review, 
                     Notification,Booking,Actor,Director,Auditorium,Producer,Payment,watchlist as Watchlist,Role,Theater,
                     RateService)
from django.contrib.auth.models import AnonymousUser
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
@permission_classes([AllowAny])
@csrf_exempt
def api_logout(request):
    """API endpoint for user logout."""
    logout(request)
    return Response({'message': 'Logout successful.'}, status=204)

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def api_user_profile(request):
    """
    GET  /api/auth/user/    → fetch profile
    PUT  /api/auth/user/    → update profile
    """
    user = request.user
    if request.method == 'GET':
        return Response(UserSerializer(user).data, status=200)

    # partial_update support
    serializer = UserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=200)

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
    @action(detail=True, methods=['get'], url_path='movies')
    def movies(self, request, pk=None):
        """Custom action to get movies featuring a specific actor."""
        actor = get_object_or_404(Actor, pk=pk)
        roles = Role.objects.filter(actor=actor)
        movies = Movie.objects.filter(roles__in=roles)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    

class DirectorViewSet(viewsets.ModelViewSet):
    """ViewSet for managing directors."""
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAdminOrReadOnly]
    @action(detail=True, methods=['get'], url_path='movies')
    def movies(self, request, pk=None):
        """Custom action to get movies directed by a specific director."""
        director = get_object_or_404(Director, pk=pk)
        movies = Movie.objects.filter(director=director)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class ProducerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing producers."""
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = [IsAdminOrReadOnly]
    @action(detail=True, methods=['get'], url_path='movies')
    def movies(self, request, pk=None):
        """Custom action to get movies produced by a specific producer."""  
        producer = get_object_or_404(Producer, pk=pk)
        movies = Movie.objects.filter(producer=producer)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing roles."""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrReadOnly]


class MovieViewSet(viewsets.ModelViewSet):
    """ViewSet for managing movies."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = [
        'title',
        'description',
        'genre__name',
        'actors__name',
        'producer__name',
        'director__name'
    ]
    filterset_fields = {
        'rating': ['exact', 'gte', 'lte'],  # filter by exact rating or ranges
        'release_date': ['exact', 'year__gte', 'year__lte'],
        'genre__name': ['exact'],
    }
    ordering_fields = ['rating', 'release_date', 'title']
    ordering = ['title']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [IsAdminOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [perm() for perm in permission_classes]
    @action(detail=False, methods=['get'], url_path='popular')
    def get_popular_movies(self, request):
        """Custom action to get popular movies."""
        popular_movies = Movie.objects.filter(rating__gte=4.0).order_by('-rating')[:10]
        serializer = self.get_serializer(popular_movies, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'], url_path='showtimes')
    def showtimes(self, request, pk=None):
        shows = Showtime.objects.filter(movie_id=pk, start_time__gte=timezone.now(),
            auditorium__available_seats__gt=0)
        serializer = ShowtimeSerializer(shows, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'], url_path='roles')
    def roles(self, request, pk=None):
        """Custom action to get roles for a specific movie."""
        movie = get_object_or_404(Movie, pk=pk)
        roles = Role.objects.filter(movie=movie)
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
# GET /api/movies/{pk}/reviews/ → list (open to all)
    @action(detail=True, methods=['get'], url_path='reviews',
            permission_classes=[AllowAny])
    def reviews(self, request, pk=None):
        qs = Review.objects.filter(movie_id=pk)
        serializer = ReviewSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    # POST /api/movies/{pk}/reviews/ → create (only auth’d)
    @reviews.mapping.post
    @permission_classes([IsAuthenticated])
    def add_review(self, request, pk=None):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, movie_id=pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields    = ['name', 'location']
    ordering_fields  = ['name', 'location']
    ordering         = ['name']

    @action(detail=True, methods=['get'], url_path='auditoriums')
    def auditoriums(self, request, pk=None):
        qs = Auditorium.objects.filter(theater_id=pk)
        serializer = AuditoriumSerializer(qs, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'], url_path='showtimes') 
    def showtimes(self, request, pk=None):
        """Custom action to get showtimes for a specific theater."""
        theater = get_object_or_404(Theater, pk=pk)
        showtimes = Showtime.objects.filter(auditorium__theater=theater, start_time__gte=timezone.now(),
            auditorium__available_seats__gt=0)
        serializer = ShowtimeSerializer(showtimes, many=True)
        return Response(serializer.data)
    

class AuditoriumViewSet(viewsets.ModelViewSet):
    """ViewSet for managing auditoriums."""
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer
    permission_classes = [IsAdminOrReadOnly]
    @action(detail=True, methods=['get'], url_path='theater')
    def get_theater(self, request, pk=None):
        """Custom action to get the theater for a specific auditorium."""
        auditorium = get_object_or_404(Auditorium, pk=pk)
        theater = auditorium.theater
        serializer = TheaterSerializer(theater)
        return Response(serializer.data)

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset         = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # keep searching by movie title / theater name
    search_fields    = ['movie__title', 'auditorium__theater__name']

    # allow URL ?start_time__date=2025-08-15&language=French&is_VIP=true
    filterset_fields = {
      'start_time':    ['date', 'gte', 'lte'],
      'language':      ['exact', 'icontains'],
      'is_VIP':        ['exact'],
      'thD_available': ['exact'],      # 3D
      'parking_available':['exact'],
      'auditorium__name': ['exact','icontains'],
      'auditorium__theater__location': ['exact','icontains'],
      'available_seats': ['gte','lte'],
    }

    # allow ?ordering=start_time or ?ordering=-available_seats
    ordering_fields  = ['start_time','available_seats','movie__rating']
    ordering         = ['start_time']
    def get_queryset(self):
        user = self.request.user
        base_qs = Showtime.objects.filter(
            start_time__gte=timezone.now(),
            auditorium__available_seats__gt=0
        )
        if user.is_staff:
            # staff still see everything
            return Showtime.objects.all()
        # everyone else only sees future, non‐sold‐out showtimes
        return base_qs
    @action(detail=True, methods=['get'], url_path='seats')
    def get_seats(self, request, pk=None):
        """Custom action to get seats for a specific showtime."""
        showtime = get_object_or_404(Showtime, pk=pk)
        seats = Seat.objects.filter(showtime=showtime)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)
    
    

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly]
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user','movie']
    search_fields    = ['content']
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Create a notification for the user
        Notification.objects.create(
            user=self.request.user,
            message=f"Your review for {serializer.validated_data['movie'].title} has been created."
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=True, methods=['get'], url_path='notifications')
    def get_notifications(self, request, pk=None):
        """Custom action to get notifications for a specific review."""
        review = get_object_or_404(Review, pk=pk)
        notifications = Notification.objects.filter(review=review)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    def perform_destroy(self, instance):
        # Create a notification for the user
        Notification.objects.create(
            user=self.request.user,
            message=f"Your review for {instance.movie.title} has been deleted."
        )
        return super().perform_destroy(instance)

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
    @action(detail=False, methods=['get'], url_path='user')
    def user(self, request):
        """
        GET /api/bookings/user/
        Returns only the bookings for the authenticated user.
        """
        qs = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.user != request.user and not request.user.is_staff:
            return Response({'error': 'You do not have permission to delete this booking.'}, status=status.HTTP_403_FORBIDDEN)
        # Ensure the booking is not in the past
        if booking.showtime.start_time < timezone.now():
            return Response({'error': 'Cannot cancel a booking for a past showtime.'}, status=status.HTTP_400_BAD_REQUEST)
        # Ensure the booking has seats
        if not booking.seats.exists():
            return Response({'error': 'No seats booked for this booking.'}, status=status.HTTP_400_BAD_REQUEST)
        num_seats = booking.seats.count()
        # Ensure the booking is not already cancelled
        if booking.status == 'Cancelled':
            return Response({'error': 'This booking has already been cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'Cancelled'
        booking.save()
        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # free the seats
            booking.seats.update(is_booked=False)
            # increment available_seats
            Showtime.objects.filter(pk=booking.showtime_id).update(
                available_seats=F('available_seats') + num_seats
            )
        booking.attended = False
        booking.status = 'Cancelled'
        booking.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        # auto‐mark all past, non‐cancelled bookings as attended
        now = timezone.now()
        Booking.objects.filter(
            showtime__start_time__lt=now,
            attended=False
        ).exclude(status='Cancelled').update(attended=True)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # also run it on retrieve so single‐item GETs stay in sync
        instance = self.get_object()
        if instance.showtime.start_time < timezone.now() \
           and instance.status != 'Cancelled' \
           and not instance.attended:
            instance.attended = True
            instance.save(update_fields=['attended'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class WatchlistViewSet(viewsets.ModelViewSet):
    """ViewSet for managing watchlists."""
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [IsWatchlistOwnerOrStaff]
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    # only allow filtering by movie; user is set from request
    filterset_fields = ['movie']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Watchlist.objects.all()
        # non-staff only see their own watchlist entries
        return Watchlist.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    



class RateServiceViewSet(viewsets.ModelViewSet):
    """
    GET  /api/rate-services/            → list (your reviews)
    POST /api/rate-services/            → create a new service‐review
    GET  /api/rate-services/{pk}/       → retrieve
    PUT/PATCH /api/rate-services/{pk}/  → update (if you allow editing)
    DELETE /api/rate-services/{pk}/     → delete
    """
    queryset          = RateService.objects.all()
    serializer_class   = RateServiceSerializer
    permission_classes = [IsAuthenticated,IsReviewOwnerOrReadOnly]
    filter_backends   = [DjangoFilterBackend]
    filterset_fields = ['booking']
    def get_queryset(self):
        user = self.request.user
        # staff see all, users only their own
        if user.is_staff:
            return RateService.objects.all()
        return RateService.objects.filter(user=user)

    def perform_create(self, serializer):
        booking = serializer.validated_data['booking']
        user = self.request.user
        # enforce only attended bookings can be reviewed
        if not booking.attended:
            raise serializers.ValidationError(
                "Can only review service for bookings you've attended."
            )
        # UniqueTogetherValidator will prevent dup on the same booking
        serializer.save(user=user, booking=booking)