from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from .tasks import (
    send_pending_booking_reminder,
    delete_unpaid_booking,
    send_showtime_reminder
)
from .permissions import (
    IsAdminOrReadOnly, IsReviewOwnerOrReadOnly, IsAuthenticated,
    IsBookingOwnerOrStaff, IsNotificationOwnerOrStaff
)
from .permissions import IsUserEmailVerified
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .serializers import (
    MovieSerializer,
    ShowtimeSerializer,
    SeatSerializer,
    GenreSerializer,
    ReviewSerializer,
    NotificationSerializer,
    BookingSerializer,
    ActorSerializer,
    DirectorSerializer,
    ProducerSerializer,
    PaymentSerializer,
    WatchlistSerializer,
    RoleSerializer,
    TheaterSerializer,
    UserSerializer,
    AuditoriumSerializer,
    RateServiceSerializer,
    FavouriteSerializer)
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db import transaction
from django.db.models import F, Count, Sum, Avg
from django.db.models.functions import TruncDate, ExtractWeekDay
from django.contrib.auth.models import User
from .models import (
    Movie,
    Genre,
    Seat,
    Showtime,
    Review,
    Notification,
    Booking,
    Actor,
    Director,
    Auditorium,
    Producer,
    Payment,
    watchlist as Watchlist,
    Role,
    Theater,
    RateService,
    Favourite)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model


def index(request):
    return render(request, 'management/index.html')


@csrf_exempt
def login_view(request, user=None):
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
            return render(request, 'management/index.html', {
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
        # Extract username, email, and password from the request
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
        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            return render(request, "management/register.html", {
                "message": "Invalid email address."
            })
        # check that the username and mail and not already in use
        if User.objects.filter(
                username=username).exists() or User.objects.filter(
                email=email).exists():
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


@api_view(['GET'])
def generate_token(request):
    # generate token
    user = request.user
    token = default_token_generator.make_token(user)
    confirm_url = request.build_absolute_uri(
        reverse('confirm-email', kwargs={'uid': user.pk, 'token': token})
    )

    # send email
    send_mail(
        subject="Confirm your account",
        message=f"Hi {user.username}, confirm your email: {confirm_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return Response(
        {"detail": "Confirmation email sent."},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def confirm_email(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return Response({"error": "Invalid link"}, status=400)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        return Response({"message": "Email confirmed successfully!"})
    return Response({"error": "Invalid or expired token"}, status=400)


# API views (login and register).
@api_view(['POST'])
def api_login(request):
    """API endpoint for user login."""
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful.'})
    else:
        return Response({'error': 'Invalid username or password.'}, status=401)


@api_view(['POST'])
def api_register(request):
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

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password)
    login(request, user)

    # Return logged-in user info (like /api/auth/user/)
    return Response({
        'message': 'Registration successful.',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def api_logout(request):
    """API endpoint for user logout."""
    logout(request)
    return Response({'message': 'Logout successful.'}, status=204)


@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def api_user_profile(request):
    """
    GET  /api/auth/user/    → fetch profile
    PUT  /api/auth/user/    → update profile
    """
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response(None, status=200)
        return Response(UserSerializer(request.user).data, status=200)
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required.'}, status=403)
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    Notification.objects.create(
        user=request.user,
        message="🔧 Your profile was updated"
    )
    return Response(serializer.data, status=200)

# API views (generic class-based or viewsets).


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

    @action(detail=True, methods=['get'], url_path='showtimes')
    def showtimes(self, request, pk=None):
        shows = Showtime.objects.filter(
            movie_id=pk,
            start_time__gte=timezone.now(),
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
        serializer = ReviewSerializer(
            qs, many=True, context={
                'request': request})
        return Response(serializer.data)

    # POST /api/movies/{pk}/reviews/ → create (only auth’d)
    @reviews.mapping.post
    @permission_classes([IsAuthenticated])
    def add_review(self, request, pk=None):
        serializer = ReviewSerializer(
            data=request.data, context={
                'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, movie_id=pk)
        # Create a notification for the user
        Notification.objects.create(
            user=request.user,
            message=f"🌟 New review for {serializer.instance.movie.title}"

        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='popular_movies')
    def popular_movies(self, request):
        popular = self.get_queryset().filter(rating__gte=4.0)
        serializer = self.get_serializer(popular, many=True)
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'location']
    ordering_fields = ['name', 'location']
    ordering = ['name']

    @action(detail=True, methods=['get'], url_path='auditoriums')
    def auditoriums(self, request, pk=None):
        qs = Auditorium.objects.filter(theater_id=pk)
        serializer = AuditoriumSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='showtimes')
    def showtimes(self, request, pk=None):
        """Custom action to get showtimes for a specific theater."""
        theater = get_object_or_404(Theater, pk=pk)
        showtimes = Showtime.objects.filter(
            auditorium__theater=theater,
            start_time__gte=timezone.now(),
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
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAdminOrReadOnly]
    # keep searching by movie title / theater name
    search_fields = ['movie__title', 'auditorium__theater__name']

    # allow URL ?start_time__date=2025-08-15&language=French&is_VIP=true
    filterset_fields = {
        'start_time': ['date', 'gte', 'lte'],
        'language': ['exact', 'icontains'],
        'is_VIP': ['exact'],
        'thD_available': ['exact'],      # 3D
        'parking_available': ['exact'],
        'auditorium__name': ['exact', 'icontains'],
        'auditorium__theater__location': ['exact', 'icontains'],
        'available_seats': ['gte', 'lte'],
    }

    # allow ?ordering=start_time or ?ordering=-available_seats
    ordering_fields = ['start_time', 'available_seats', 'movie__rating']
    ordering = ['start_time']

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
    permission_classes = [IsReviewOwnerOrReadOnly, IsUserEmailVerified]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'movie']
    search_fields = ['content']

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        Notification.objects.create(
            user=self.request.user,
            message=f"Your review for {review.movie.title} has been created."
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        # only save the provided fields; user already set on create
        review = serializer.save()
        Notification.objects.create(
            user=self.request.user,
            message=f"✏️ Review updated for {review.movie.title}"
        )

    def perform_destroy(self, instance):
        # Create a notification for the user
        Notification.objects.create(
            user=self.request.user,
            message=f"Your review for {instance.movie.title} has been deleted."
        )
        return super().perform_destroy(instance)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsNotificationOwnerOrStaff]

    def get_queryset(self):
        # only this user’s notifications
        return Notification.objects.filter(
            user=self.request.user).order_by('-created_at')

    def partial_update(self, request, *args, **kwargs):
        # guard object‐level perms
        notif = self.get_object()
        if notif.user != request.user:
            raise PermissionDenied("Cannot mark another user's notification")
        return super().partial_update(request, *args, **kwargs)


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bookings."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [
        IsBookingOwnerOrStaff,
        IsAuthenticated,
        IsUserEmailVerified]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        Notification.objects.create(
            user=self.request.user,
            message=f"✅ Booking created for {booking.showtime.movie.title}"
        )
        # 1) remind in 24 h if still pending
        send_pending_booking_reminder.apply_async(
            args=[booking.id],
            countdown=86400,  # 24*60*60 seconds
        )

        # 2) delete in 48 h if still pending
        delete_unpaid_booking.apply_async(
            args=[booking.id],
            countdown=86400 * 2,
        )

        # 3) 24 h before showtime (only if that time is in the future)
        eta = booking.showtime.start_time - timedelta(hours=24)
        if eta > timezone.now():
            send_showtime_reminder.apply_async(
                args=[booking.id],
                eta=eta,
            )

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
            return Response(
                {
                    'error': 'You do not have permission to delete this booking.'},
                status=status.HTTP_403_FORBIDDEN)
        # Ensure the booking is not in the past
        if booking.showtime.start_time < timezone.now():
            return Response({'error': 'Cannot cancel a booking for a past showtime.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Ensure the booking has seats
        if not booking.seats.exists():
            return Response({'error': 'No seats booked for this booking.'},
                            status=status.HTTP_400_BAD_REQUEST)
        num_seats = booking.seats.count()
        # Ensure the booking is not already cancelled
        if booking.status == 'Cancelled':
            return Response({'error': 'This booking has already been cancelled.'},
                            status=status.HTTP_400_BAD_REQUEST)
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
        Notification.objects.create(
            user=request.user,
            message=f"❌ Booking cancelled for {booking.showtime.movie.title}"
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
            attended=False,
            status__in=['Confirmed']
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

    def perform_update(self, serializer):
        booking = serializer.save()
        Notification.objects.create(
            user=self.request.user,
            message=f"✏️ Booking updated for {booking.showtime.movie.title}"
        )
        return booking


class WatchlistViewSet(viewsets.ModelViewSet):
    """ViewSet for managing watchlists."""
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    # only allow filtering by movie; user is set from request
    filterset_fields = ['user', 'movie']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Watchlist.objects.all()
        # non-staff only see their own watchlist entries
        return Watchlist.objects.filter(user=user)

    def perform_create(self, serializer):
        new = serializer.save(user=self.request.user)
        Notification.objects.create(
            user=self.request.user,
            message=f"⭐ Added {new.movie.title} to your watchlist"
        )

    def perform_destroy(self, instance):
        title = instance.movie.title
        instance.delete()
        Notification.objects.create(
            user=self.request.user,
            message=f"🗑 Removed {title} from your watchlist"
        )


class RateServiceViewSet(viewsets.ModelViewSet):
    """
    GET  /api/rate-services/            → list (your reviews)
    POST /api/rate-services/            → create a new service‐review
    GET  /api/rate-services/{pk}/       → retrieve
    PUT/PATCH /api/rate-services/{pk}/  → update (if you allow editing)
    DELETE /api/rate-services/{pk}/     → delete
    """
    queryset = RateService.objects.all()
    serializer_class = RateServiceSerializer
    permission_classes = [IsAuthenticated, IsReviewOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
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
        Notification.objects.create(
            user=user,
            message=f"🌟 New review for {booking.showtime.movie.title}"
        )
        serializer.save(user=user, booking=booking)


class FavouriteViewSet(viewsets.ModelViewSet):
    """ViewSet for managing favourites."""
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Favourite.objects.all()
        return Favourite.objects.filter(user=user)

    def perform_create(self, serializer):
        fav = serializer.save(user=self.request.user)
        Notification.objects.create(
            user=self.request.user,
            message=f"❤️ You favorited {fav.movie.title}"
        )

    def perform_destroy(self, instance):
        title = instance.movie.title
        super().perform_destroy(instance)
        Notification.objects.create(
            user=self.request.user,
            message=f"💔 You unfavorited {title}"
        )


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['booking']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='process')
    def process_payment(self, request):
        # debug print so you see the payload
        print("🔔 process_payment called:", request.data)
        booking_id = request.data.get('booking_id')
        if not booking_id:
            return Response(
                {"detail": "booking_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            booking = get_object_or_404(
                Booking, pk=booking_id, user=request.user)

            if booking.status != 'Pending':
                return Response(
                    {"detail": "Booking already paid or cancelled"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if hasattr(booking, 'payment'):
                return Response(
                    {"detail": "Payment already exists for this booking."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # mock “charge”
            payment = Payment.objects.create(
                user=request.user,
                booking=booking,
                amount=booking.cost,
                status="success"
            )

            booking.status = "Confirmed"
            booking.save(update_fields=["status"])
            Notification.objects.create(
                user=request.user, message=f"💳 Payment received for booking #"
                f"{payment.booking.showtime.movie.title}")
            return Response(
                {"payment_id": payment.id, "status": "success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # print full traceback to your runserver console
            import traceback
            traceback.print_exc()
            # return the exception message in JSON so you see it in the browser
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        User = get_user_model()  # Use the custom user model
        now = timezone.now()
        week_ago = now - timezone.timedelta(days=7)
        month_ago = now - timezone.timedelta(days=30)

        # --- existing users / growth stats ---
        total_users = User.objects.count()
        new_week = User.objects.filter(date_joined__gte=week_ago).count()
        new_month = User.objects.filter(date_joined__gte=month_ago).count()
        active_users = User.objects.filter(is_active=True).count()
        verified_emails = User.objects.filter(
            is_active=True, email_verified=True).count()

        # --- Conversion funnel ---
        registered = total_users
        verified = verified_emails
        booked = Booking.objects.filter(
            status__in=[
                'Pending',
                'Confirmed']).values('user').distinct().count()
        paid = Payment.objects.filter(status='Completed').values(
            'booking__user').distinct().count()
        funnel = {
            "registered": registered,
            "verified": verified,
            "booked": booked,
            "paid": paid,
        }

        # retention vs churn
        old_users = User.objects.filter(date_joined__lte=month_ago)
        booked_old = old_users.filter(
            bookings__created_at__gte=month_ago).distinct().count()
        retention_rate = booked_old / old_users.count() if old_users.exists() else 0

        # top 5 users by points
        top_users_qs = User.objects.annotate(
            total_points=Sum('points')).order_by('-total_points')[:5]
        top_users = [{'id': u.id, 'username': u.username,
                      'total_points': u.total_points or 0} for u in top_users_qs]

        # daily growth trend (last 30 d)
        growth = (
            User.objects.filter(date_joined__gte=month_ago)
            .annotate(day=TruncDate('date_joined'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # --- booking stats ---
        total_bookings = Booking.objects.count()
        pending = Booking.objects.filter(status='Pending').count()
        confirmed = Booking.objects.filter(status='Confirmed').count()
        cancelled = Booking.objects.filter(status='Cancelled').count()
        attended = Booking.objects.filter(attended=True).count()

        # Repeat vs one-time customers
        repeat_customers = (
            User.objects.annotate(bcount=Count('bookings'))
            .filter(bcount__gt=1).count()
        )
        one_time_customers = (
            User.objects.annotate(bcount=Count('bookings'))
            .filter(bcount=1).count()
        )

        # average lead‐time (booking → showtime) in hours
        lead_times = Booking.objects.filter(status='Confirmed')\
            .annotate(lead=F('showtime__start_time') - F('created_at'))\
            .aggregate(avg_lead=Avg('lead'))['avg_lead']
        avg_lead_hours = (
            lead_times.total_seconds() /
            3600) if lead_times else 0

        # bookings by day of week
        dow = (
            Booking.objects.annotate(dow=ExtractWeekDay('created_at'))
            .values('dow').annotate(count=Count('id')).order_by('dow')
        )

        # --- Global occupancy (all showtimes) ---
        total_seats = Seat.objects.count()  # all seats
        booked_seats = Seat.objects.filter(
            is_booked=True).count()  # all booked seats
        occupancy_rate = booked_seats / total_seats if total_seats else 0

        # --- Auditorium utilization (per hall) ---
        auditoriums = Auditorium.objects.all()
        auditorium_utilization = []

        for aud in auditoriums:
            pass

        # --- revenue ---
        total_revenue = Payment.objects.filter(
            status='Completed').aggregate(
            sum=Sum('amount'))['sum'] or 0
        refunds = Payment.objects.filter(
            status='Refunded').aggregate(
            sum=Sum('amount'))['sum'] or 0
        failed = Payment.objects.filter(status__in=['Failed', 'Error']).count()

        # revenue by movie
        rev_by_movie = (
            Payment.objects.filter(status='Completed')
            .values('booking__showtime__movie__title')
            .annotate(revenue=Sum('amount'))
            .order_by('-revenue')[:10]
        )

        # Revenue trend (last 30 days)
        revenue_trend = (
            Payment.objects.filter(
                status="Completed",
                created_at__gte=month_ago) .annotate(
                day=TruncDate("created_at")) .values("day") .annotate(
                total=Sum("amount")) .order_by("day"))

        # --- movie analytics ---
        top_movies = Movie.objects.annotate(booked=Count(
            'showtimes__bookings')).order_by('-booked')[:5]
        top_movies_data = [{'title': m.title, 'bookings': m.booked}
                           for m in top_movies]

        top_rated = (
            Review.objects.values('movie__title')
            .annotate(avg=Avg('rating'), cnt=Count('id'))
            .filter(cnt__gte=5)
            .order_by('-avg')[:5]
        )

        most_reviewed = sorted(
            [{'title': r['movie__title'], 'reviews': r['cnt']} for r in top_rated],
            key=lambda x: -x['reviews']
        )[:5]
        top_favorited = (
            Favourite.objects.values('movie__title')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        Favourite_data = [{'title': f['movie__title'],
                           'favorited': f['count']} for f in top_favorited]
        top_watchlisted = Movie.objects.annotate(
            watched=Count('watchlists')).order_by('-watched')[:5]
        watchlist_data = [{'title': m.title, 'watchlisted': m.watched}
                          for m in top_watchlisted]

        # --- service review analytics ---
        svc_aud_qs = RateService.objects.values(
            aud_id=F('booking__showtime__auditorium__id'),
            aud_name=F('booking__showtime__auditorium__name'),
        ).annotate(avg_rating=Avg('all_rating')).order_by('-avg_rating')
        service_by_auditorium = [
            {
                "auditorium_id": r['aud_id'],
                "auditorium": r['aud_name'],
                "average_rating": float(
                    r['avg_rating'] or 0)} for r in svc_aud_qs]

        svc_th_qs = RateService.objects.values(
            th_id=F('booking__showtime__auditorium__theater__id'),
            th_name=F('booking__showtime__auditorium__theater__name'),
        ).annotate(avg_rating=Avg('all_rating')).order_by('-avg_rating')
        service_by_theater = [
            {"theater_id": r['th_id'], "theater": r['th_name'], "average_rating": float(r['avg_rating'] or 0)}
            for r in svc_th_qs
        ]

        return Response({
            "users": {
                "total": total_users,
                "new_7d": new_week,
                "new_30d": new_month,
                "active": active_users,
                "verified_email": verified_emails,
                "retention_rate": retention_rate,
                "top_by_points": top_users,
                "growth_trend_30d": list(growth),
                "funnel": funnel,
            },
            "bookings": {
                "total": total_bookings,
                "pending": pending,
                "confirmed": confirmed,
                "cancelled": cancelled,
                "attended": attended,
                "avg_lead_hours": avg_lead_hours,
                "by_day_of_week": list(dow),
                "occupancy_rate": occupancy_rate,
                "repeat_customers": repeat_customers,
                "one_time_customers": one_time_customers,
                "auditorium_utilization": auditorium_utilization,
            },
            "revenue": {
                "total": total_revenue,
                "refunds": refunds,
                "failed_count": failed,
                "by_movie": list(rev_by_movie),
                "trend_30d": list(revenue_trend),
            },
            "movies": {
                "top_booked": top_movies_data,
                "top_rated": list(top_rated),
                "most_reviewed": most_reviewed,
                "top_watchlisted": watchlist_data,
                "top_favorited": list(Favourite_data),
            },
            "service_reviews": {
                "by_auditorium": service_by_auditorium,
                "by_theater": service_by_theater,
            },
        })
