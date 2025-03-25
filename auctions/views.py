from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import User, Auction, Comment,Bid, Category
from django.contrib.auth import update_session_auth_hash


 #Show all active auctions on the index page 
 # Or search for a specific auction (search by title)
def index(request):
    if request.GET.get("q"):
        return HttpResponseRedirect(reverse("search"))
    auctions = Auction.objects.all().filter(active=True)
    return render(request, "auctions/index.html", {
                "auctions": auctions
            })


# Search for an auction by title (check if the title contains the query)
# Display the search results
def search(request):
    query = request.GET.get("q", "").strip()  # Ensure query is not None
    auctions = Auction.objects.filter(title__icontains=query ,active=True ) if query else [] 
    return render(request, "auctions/search.html", {
        "auctions": auctions
    })


# Show the listing page of a specific auction
# Allow users to bid, comment, add to watchlist, and close the auction
# If the auction is closed, redirect to a closed page
# If the user is not authenticated, display the listing page without the bid, comment, and watchlist features
# If the user is authenticated, display the listing page with all features
# If the page is closed and the user is the highest bidder, display a message
def listingPage(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if not auction.active:
          return render(request, "auctions/closedPage.html", {
                "auction": auction
            })
    User = request.user
    if User.is_authenticated:
        if request.method == "POST":
            if request.POST.get("bid"):
                if User== auction.user:
                    return render(request, "auctions/listingPage.html", {
                        "auction": auction,
                        "message": "You cannot bid on your own auction"
                    })
                if User == auction.current:
                    return render(request, "auctions/listingPage.html", {
                        "auction": auction,
                        "message": "You are already the highest bidder"
                    })
                bid = request.POST["bid"]
                if Decimal(bid) > auction.starting_bid:
                    auction.starting_bid = bid
                    auction.current = User
                    auction.save()
                    Bid.objects.create(value=bid, user=User, auction=auction)
                else:   
                    return render(request, "auctions/listingPage.html", {
                        "auction": auction,
                        "message": "Bid must be higher than the starting bid"
                    })
            if request.POST.get("comment"): 
                comment = request.POST["comment"]
                comment=Comment(text=comment, user=User, auction=auction)
                comment.save()
            if request.POST.get("watchlist") == "add":
                User.watchlist.add(auction)
            if request.POST.get("watchlist") == "remove":
                User.watchlist.remove(auction)
            if request.POST.get("close") == "close":
                auction.active = False
                winner =auction.current
                if winner != None:
                    winner.won_auctions.add(auction)
                auction.save()
                return HttpResponseRedirect(reverse("index"))
            watchlist = User.watchlist.filter(pk=auction_id).exists()
            comments = Comment.objects.all().filter(auction=auction)
            return render(request, "auctions/listingPage.html", {
                "auction": auction,
                "watchlist": watchlist,
                "comments": comments
            })
        # Check if auction is in the user's watchlist (for GET request)
        watchlist = User.watchlist.filter(pk=auction_id).exists()
        comments = Comment.objects.all().filter(auction=auction)
        return render(request, "auctions/listingPage.html", {
                "auction": auction,
                "watchlist": watchlist,
                "comments": comments
            })
    else:
        
        return render(request, "auctions/listingPage.html", {
            "auction": auction
        })


# Show the login page
# Allow users to log in
# If the user is authenticated, redirect to the index page
# If the user is not authenticated, display the login page
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if not password or not username:
            return render(request, "auctions/login.html", {
                "message": "Please fill out all fields."
            })
        # Check if authentication successful
        if user is not None:
            login(request, user)
            auctions= user.auctions.all().filter(active=True)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# Log out the user
# Redirect to the index page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Show the registration page
# Allow users to register
# If the user is authenticated, redirect to the index page
# If the user is not authenticated, display the registration page
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if not password or not confirmation or not username or not email:
            return render(request, "auctions/register.html", {
                "message": "Please fill out all fields."
            })
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Create a new auction
# Allow users to create a new auction
# If the user is authenticated, display the create page
@login_required
def create(request):
    if request.method == "POST":
        
        if request.POST.get("category"):
            category=Category.objects.get(id=request.POST.get("category"))
        else:
            category=Category.objects.get(name="Other")
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = None
        if  request.POST["image_url"]:
            image = request.POST["image_url"]
        user = request.user
        auction = Auction(title=title, description=description, starting_bid=starting_bid, image=image, category=category, user=user, active=True, current=None)
        auction.save()
        return HttpResponseRedirect(reverse("index"))
    else:    
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })


# Show the watchlist page
@login_required
def watchlist(request):
    User = request.user
    watchlist = User.watchlist.all().filter(active=True)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


# Show all categories
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
  

# Show all auctions in a specific category  
def category(request, category):
    category = Category.objects.get(name=category)
    category_id = category.id 
    auctions = Auction.objects.all().filter(category=category_id, active=True)
    return render(request, "auctions/category.html", {
        "category": category,
        "auctions": auctions,
        
    })


# Show the profile page
# Display the user's auctions, won auctions, comments, and bids
@login_required
def profile(request):
    User = request.user
    auctions = User.auctions.all()
    won = User.won_auctions.all().filter(active=False)
    comments=Comment.objects.all().filter(user=User)
    bids = Bid.objects.all().filter(user=User)
    return render(request, "auctions/profile.html", {
        "auctions": auctions,
        "won": won,
        "comments": comments,
        "bids": bids
    })


# Show closed page
def closed(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    return render(request, "auctions/listingPage.html", {
        "auction": auction
    })


# Change the user's password
# If the password is invalid, display a message
# If the passwords do not match, display a message
# If the password is not at least 8 characters long, display a message
# If the password is changed successfully, display a message
@login_required
def changePassword(request):
    if request.method == "POST":
        user = request.user
        password = request.POST["old_password"]
        if not user.check_password(password):
            return render(request, "auctions/changePassword.html", {
                "message": "Invalid password."
            })
        new_password = request.POST["new_password"]
        confirmation = request.POST["new_password2"]
        if new_password != confirmation:
            return render(request, "auctions/changePassword.html", {
                "message": "Passwords must match."
            })
        if not user.set_password(new_password):
            return render(request, "auctions/changePassword.html", {
                "message": "Password must be at least 8 characters long."
            })
        user.save()
        update_session_auth_hash(request, user) 
        return render(request, "auctions/changePassword.html", {
            "message": "Password changed successfully."
        })
    else:
        return render(request, "auctions/changePassword.html")
    

# Add a new category
# If the category already exists, display a message
# If the category name is empty, display a message
# If the category is created successfully, redirect to the create page
@login_required    
def addCategory(request):
    if request.method == "POST":
        new_category = request.POST.get("new_category", "").strip()
        
        if new_category:
            # Check if the category already exists
            if Category.objects.filter(name=new_category).exists():
                return render(request, "auctions/addCategory.html", {
                    "message": f"Category '{new_category}' already exists."
                })
            else:
                # Create the new category
                Category.objects.create(name=new_category)
                return HttpResponseRedirect(reverse("create"))  # Redirect to the create page
        else:
         return render(request, "auctions/addCategory.html", {
            "message": "Category name cannot be empty."
        })
    else:
        return render(request, "auctions/addCategory.html")
        

# Show the user's bids page
@login_required      
def bids(request):
    User = request.user
    bids = Bid.objects.all().filter(user=User)
    return render(request, "auctions/bids.html", {
        "bids": bids
    })


# Show the user's auctions page
@login_required
def auctions(request):
    User = request.user
    auctions = User.auctions.all()
    return render(request, "auctions/listing.html", {
        "auctions": auctions
    })


# Show the user's won auctions page
@login_required
def won(request):
    User = request.user
    won = User.won_auctions.all().filter(active=False)
    return render(request, "auctions/won.html", {
        "won": won
    })


# Show the user's comments page
@login_required
def comments(request):
    User = request.user
    comments = Comment.objects.all().filter(user=User)
    return render(request, "auctions/comments.html", {
        "comments": comments
    })