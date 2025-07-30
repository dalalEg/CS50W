from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import User, Movie, Booking, Showtime, Seat,Genre,Review,Notification

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