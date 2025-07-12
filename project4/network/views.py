from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User ,Post, Follow, Like, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import json
from random import sample

def index(request):
    return render(request, "network/index.html")


@csrf_exempt
def login_view(request):
    """Log user in."""
    # If the request method is POST, attempt to log the user in
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # If username and password not provided, return error
        if not username or not password:
            return render(request, "network/login.html", {
                "message": "Username and password are required."
            })
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

# Logout view
@login_required
def logout_view(request):
    """Log user out."""
    # If the request method is POST, log the user out
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
            return render(request, "network/register.html", {
                "message": "All fields are required."
        })
      
        # check that the email is valid 
        if not email or '@' not in email or '.' not in email.split('@')[-1] :
            return render(request, "network/register.html", {
                "message": "Invalid email address."
            })
        # check that the username and mail and not already in use
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, "network/register.html", {
                "message": "Username or email already taken."
            })
        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        try:        # Attempt to create new user

            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

## View to handle posts
def posts(request):
    """Handles the creation and retrieval of posts.
    If the user is authenticated and the request method is GET, it returns all posts.
    If the request method is POST, it creates a new post with the provided content.
    """
    if not request.user.is_authenticated or  request.method == "GET": 
        # Return all posts
        posts = Post.objects.all().order_by('-created_at')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = []
        # Serialize the posts
        for post in page_obj:   
            data.append({
                "id": post.id,
                "user": post.user.username,
                "content": post.content,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
                "likes_count": post.likes_count,
                "updated_at": post.updated_at.strftime("%Y-%m-%d %H:%M"),
                "is_liked": Like.objects.filter(user=request.user, post=post).exists() if request.user.is_authenticated else False,
            })
        return JsonResponse({
            "posts": data,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        })
    elif request.method == "POST":
        # Create a new post
        try:
            data = json.loads(request.body)
            content = data.get("content", "").strip()
            if not content: # Check if content is empty
                return JsonResponse({"error": "Content cannot be empty."}, status=400)
            
            post = Post(user=request.user, content=content)
            post.save() # Save the post to the database
            return JsonResponse(post.serialize(), status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@login_required
def profile(request):
    """Return the profile of the logged-in user."""
    user = User.objects.get(username=request.user.username)
    all_param = request.GET.get('all')
    if all_param == 'true':
        posts = Post.objects.filter(user=user).order_by('-created_at')
        return JsonResponse({
            "all_posts": [post.serialize() for post in posts]
        })
    if request.method == "GET":
        # Return the profile of the logged-in user
        user = User.objects.get(username=request.user.username)
        posts = Post.objects.filter(user=user).order_by('-created_at')
        followers= Follow.objects.filter(following=user).count()
        following = Follow.objects.filter(follower=user).count()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Check if the user is following anyone
        following_ids = set(Follow.objects.filter(follower=user).values_list('following__id', flat=True))
        # If the user is following no one, show random users
        exclude_ids = following_ids | {user.id}
        candidates = User.objects.exclude(id__in=exclude_ids)
        candidate_usernames = list(candidates.values_list('username', flat=True))
        random_usernames = sample(candidate_usernames, min(5, len(candidate_usernames)))  # Show up to 5 random users

        #all_users = all_users.exclude(username=request.user.username)  # Exclude the current user
        return JsonResponse({
            "username": user.username,
            "email": user.email,
            "posts": [post.serialize() for post in page_obj],
            "followers": followers,
            "following": following,
            "random_users": random_usernames,
            "followers_list": [f.follower.username for f in Follow.objects.filter(following=user)],
            "following_list": [f.following.username for f in Follow.objects.filter(follower=user)],
        }, safe=False)

def other_profile(request, username):
    """Return the profile of another user."""
    # If the request method is GET, return the profile of the user with the given username
    # If the request method is POST, follow the user with the given username
    # If the request method is DELETE, unfollow the user with the given username
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
            posts = Post.objects.filter(user=user).order_by('-created_at')
            followers = Follow.objects.filter(following=user).count()
            following = Follow.objects.filter(follower=user).count()
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            is_following = False
            is_their_profile = False
            if request.user.is_authenticated:
                is_following = Follow.objects.filter(follower=request.user, following=user).exists()
                is_their_profile = request.user.username == username
            return JsonResponse({
                "username": user.username,
                "email": user.email,
                "posts": [post.serialize() for post in page_obj],
                "followers": followers,
                "following": following,
                "is_following": is_following,
                "is_their_profile": is_their_profile,
                "followers_list": [f.follower.username for f in Follow.objects.filter(following=user)],
                "following_list": [f.following.username for f in Follow.objects.filter(follower=user)],
            }, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
    else:    #follow or unfollow a user
        if not request.user.is_authenticated: # Check if the user is authenticated
            # If not authenticated, return an error
            return JsonResponse({"error": "Authentication required."}, status=401)

        try:
            user = User.objects.get(username=username) # Get the user with the given username
            if request.method == "POST":
              
                # Follow the user
                follow, created = Follow.objects.get_or_create(follower=request.user, following=user)
                if created:
                    return JsonResponse({"message": f"You are now following {username}."}, status=201)
                else:
                    return JsonResponse({"message": f"You are already following {username}."}, status=200)
            elif request.method == "DELETE":
                # Unfollow the user
                follow = Follow.objects.filter(follower=request.user, following=user).first()
                if follow:
                    follow.delete()
                    return JsonResponse({"message": f"You have unfollowed {username}."}, status=200)
                else:
                    return JsonResponse({"error": "You are not following this user."}, status=404)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
@login_required
def following(request):
    """Return the posts of users that the logged-in user is following."""
    # If the request method is GET, return the posts of users that the logged-in user is following
    if request.method == "GET":
        # Return the list of users that the logged-in user is following
        if not request.user.is_authenticated: # Check if the user is authenticated
            # If not authenticated, return an error
            return JsonResponse({"error": "Authentication required."}, status=401)

        following = Follow.objects.filter(follower=request.user)
        posts = Post.objects.filter(user__in=[follow.following for follow in following]).order_by('-created_at')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = []
        # Serialize the posts
        for post in page_obj:
            data.append({
                "id": post.id,
                "user": post.user.username,
                "content": post.content,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
                "likes_count": post.likes_count,
                "updated_at": post.updated_at.strftime("%Y-%m-%d %H:%M"),
                "is_liked": Like.objects.filter(user=request.user, post=post).exists() if request.user.is_authenticated else False,
            })
        return JsonResponse({
            "posts": data,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        })
@login_required
def like_post(request, post_id):
    """Like or unlike a post."""
    # If the user is not authenticated, return an error
     # If the post does not exist, return an error
    # If the request method is POST, like the post
    # If the request method is DELETE, unlike the post
    # Always return the current state of the post
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required."}, status=401)
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "POST":
        # Like the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            post.likes_count += 1
            post.save()
        # Always return the current state
        return JsonResponse({
            "message": "Post liked.",
            "likes_count": post.likes_count,
            "is_liked": True
        }, status=201)

    elif request.method == "DELETE":
        # Unlike the post
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            post.likes_count -= 1
            post.save()
        # Always return the current state
        return JsonResponse({
            "message": "Post unliked.",
            "likes_count": post.likes_count,
            "is_liked": False
        }, status=200)
    

def post(request, post_id):
    """Handle individual post actions such as viewing, editing, and deleting."""
    # If the request method is GET, return the post details
    # If the request method is PUT, update the post content
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_owner = user.is_authenticated and post.user == user
    is_liked = user.is_authenticated and Like.objects.filter(user=user, post=post).exists()
    can_like = user.is_authenticated  # User can like if authenticated

    # User can edit if they are the owner of the post
    can_edit = is_owner
    if request.method == "GET":
        return JsonResponse({
            "id": post.id,
            "user": post.user.username,
            "content": post.content,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": post.updated_at.strftime("%Y-%m-%d %H:%M"),
            "likes_count": post.likes_count,
            "is_liked": is_liked,
            "can_like": can_like,
            "can_edit": True if can_edit else False,

        })
    elif request.method == "PUT" and can_edit:
        data = json.loads(request.body)
        post.content = data.get("content", post.content)
        post.updated_at = timezone.now()  # Update the timestamp
        if not post.content.strip():
            return JsonResponse({"error": "Content cannot be empty."}, status=400)
        # Save the updated post
        post.save()
        return JsonResponse({"content": post.content})
    elif request.method == "DELETE":
        # Delete the post (not implemented yet)
        post.delete()
        return JsonResponse({"message": "Post deleted."}, status=204)
    
def spa_shell(request):
    return render(request, "network/index.html")

def userPosts(request, username):
    """Return the posts of a specific user."""
    # If the request method is GET, return the posts of the user with the given username
    try:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user).order_by('-created_at')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = []
        for post in page_obj:
            data.append({
                "id": post.id,
                "user": post.user.username,
                "content": post.content,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
                "likes_count": post.likes_count,
                "updated_at": post.updated_at.strftime("%Y-%m-%d %H:%M"),
                "is_liked": Like.objects.filter(user=request.user, post=post).exists() if request.user.is_authenticated else False,
            })
        return JsonResponse({
            "username": user.username,
            "posts": data,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        })
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    

def comment(request, post_id):
    """Handle comments on a post.
    If the request method is GET, return all comments for the post.
    If the request method is POST, create a new comment on the post.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == "GET":
        comments = post.comments.order_by('created_at')
        return JsonResponse({"comments": [c.serialize() for c in comments]})
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required."}, status=401)
        data = json.loads(request.body)
        content = data.get("content", "").strip()
        if not content:
            return JsonResponse({"error": "Comment cannot be empty."}, status=400)
        comment = Comment.objects.create(user=request.user, post=post, content=content)
        return JsonResponse(comment.serialize(), status=201)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)
    

def user_comments(request, username):
    """Return the comments made by a specific user."""
    # If the request method is GET, return the comments made by the user with the given username
    try:
        user = User.objects.get(username=username)
        comments = Comment.objects.filter(user=user).order_by('-created_at')
        paginator = Paginator(comments, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = [comment.serialize() for comment in page_obj]
        return JsonResponse({
            "username": user.username,
            "comments": data,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        })
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)


def user_likes(request, username):
    """Return the likes made by a specific user."""
    # If the request method is GET, return the likes made by the user with the given username
    try:
        user = User.objects.get(username=username)
        likes = Like.objects.filter(user=user).order_by('-created_at')
        paginator = Paginator(likes, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = [
            {
                "post_id": like.post.id,
                "post_content": like.post.content,
                "user": like.post.user.username,
                "liked_at": like.post.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for like in page_obj
        ]
        return JsonResponse({
            "username": user.username,
            "likes": data,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        })
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
def search(request):
    """Search for users or posts based on the query parameter."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required."}, status=400)

    # Search for users
    users = User.objects.filter(username__icontains=query)
    user_results = [{"username": user.username, "email": user.email} for user in users]

    # Search for posts
    posts = Post.objects.filter(content__icontains=query).order_by('-created_at')
    post_results = [post.serialize() for post in posts]

    return JsonResponse({
        "users": user_results,
        "posts": post_results
    })