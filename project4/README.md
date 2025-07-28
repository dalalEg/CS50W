# 📱 Social Network - CS50 Web Project 4

This is a Django-based social network web application that allows users to post content, follow others, like and comment on posts, and interact in a real-time-like environment. The project is built using **Python**, **Django**, **JavaScript**, **HTML**, and **CSS** as part of the [CS50 Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/) course.

## 🚀 Features

### 🔹 Authentication
- Register, login, and logout functionality.
- Only authenticated users can post, like, follow/unfollow, and comment.

### 🔹 Create & View Posts
- Authenticated users can submit text-based posts.
- Posts include:
  - Poster’s username (clickable to visit profile)
  - Timestamp (e.g., "1 hour ago")
  - Number of likes and comments

### 🔹 Feed Pages
- **All Posts**: Shows all user posts in reverse chronological order.
- **Following**: Shows only posts from users the current user follows.
- Both views support:
  - **Pagination** (10 posts per page)
  - **Like/Unlike** functionality via JavaScript (no page reload)
  - **Commenting** on posts with real-time feedback

### 🔹 Profile Pages
- Click a username anywhere to view that user’s profile.
- Shows:
  - Follower and following counts
  - List of user’s posts (reverse chronological)
  - Like and comment counts per post
  - “Follow” / “Unfollow” button (if viewing another user)
  - **User Recommendations** (for the current user, shows suggestions to follow)
  - List of followers and following usernames

### 🔹 Edit Posts
- Users can edit their own posts.
- In-place editing with a **textarea** and **Save** button using JavaScript (no reload).
- Server-side protection to ensure users cannot edit others’ posts.

### 🔹 Search
- Search bar allows:
  - Searching for **users** by username
  - Searching for **posts** containing keywords
- Results include matching usernames or posts.

## 🛠️ Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (default Django setup)
- **Design**: Bootstrap 4

## 📁 File Structure
  project4/
  │
  ├── network/ # Django app with models, views, and logic
  ├── project4/ # Django project settings and URLs
  ├── manage.py # Django management script

## 💡 Extras
- "Time ago" timestamps (e.g., "2 hours ago", "yesterday").
- Asynchronous operations for liking, editing, and commenting.
- Search results also show user follow/follower details.

## 📷 Demo Video
https://www.youtube.com/watch?v=TELOnfr8meY
## 📌 Notes
- Be sure to run migrations and create a superuser if testing locally.
