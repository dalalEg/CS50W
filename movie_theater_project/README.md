🎬 Movie Theater Web App

A full-stack web application for booking movie tickets — featuring dynamic seat selection, user reviews, rich search & filtering, and an admin management system. Built with Django REST Framework and React.

⚠️ Actively developed – frontend and backend integration in progress.




# 🛠 Features
- 🔐 User Authentication – Register, login, logout with secure session handling.

- 🔍 Advanced Search & Filters – Search by title, genre, rating, year, duration, or theater.

- 🎬 Movie Browsing – View trailers, posters, credits, and details.

- 🎟️ Seat Selection – Interactive seat picker tied to showtimes.

- 🧾 Booking System – Automatic user linking, confirmation, and reservation management.

- ⭐ Movie Reviews – Public reviews & ratings for each movie.

- ⭐ Service Reviews – Time-gated reviews available only after attending a booked showtime.

- 📌 Watchlist & Favorites – Save movies and get updates on similar content.
- 📣 Notifications – Alerts for bookings, favorites, and new showtimes.

- 👤 User Profile – Centralized history of bookings, reviews, and saved lists.

- 🏛️ Theaters & Auditoriums – Directory with venue details.

- 🛠️ Admin Panel – Manage movies, showtimes, cast, and production details.

- 🐳 Dockerized Setup – Containerized for easy deployment (in progress).

- ⚙️ CI/CD with GitHub Actions – Automated testing & deployment (in progress).

- 🔔 Coming Soon Alerts – Get notified about upcoming movies (planned).

- 🗳️ Feature Voting System – Users can vote on new features or retro requests (planned).
# 🛠️ Tech Stack


- Backend: Django + Django REST Framework with PostgreSQL.

- Frontend: React + Axios + React Router + Bootstrap 

- Database: PostgreSQL

- Auth: Django sessions

- Dockerized: Full stack runs via Docker Compose (backend, frontend, DB).

- CI/CD Pipeline:

- Django tests (models, API endpoints).

- React tests (Jest + RTL for core components).

- Code linting (flake8/black, eslint/prettier).

- Media Handling: Posters and images served correctly in Docker environment.



# 🚧 Roadmap
## ✅ Done

- 🎯 Feature set & roadmap defined

- 🧱 DB schema (Movie, Seat, Showtime, Booking, Actor, Director, Producer, Theater, Auditorium)

- 🔧 Django models + migrations

- 👩‍💻 Seeded test data (genres, movies, theaters)

- 🔌 REST API with DRF

- 🔐 Auth: login/register/logout (Django backend + React frontend)

- 🎞️ List all movies

- 📅 Show available showtimes (future only, with > 0 seats)

- 👤 Profile API (authenticated user)

- 🎭 Actor/Director/Genre/Producer management via API

- 🏗️ React app setup (routing, Axios, proxy)

- 🔗 Frontend ↔ Backend integration

- 📱 Mobile-responsive layout (Bootstrap)

- 🎥 Movie Detail page (trailer, actors, reviews, showtimes)

- 🪑 Showtime detail with visual seat map

- 🏛️ Our Theaters page (theaters & auditoriums)

- 🧾 Booking logic + confirmation UI (click-through to details)

- ⭐ Review system (with edit/delete and anonymous toggle)

- 🛒 End-to-end booking flow (showtime → seats → confirmation)

- ➕ Detail pages: Directors, Actors, Producers, Theaters

- 🔍 Search & filters for movies/showtimes/theaters
-  (genre, rating, year, duration, sort, keyword)

- 👤 Polished profile UI (bookings, reviews,watchlist)
- 🗑️ Booking cancellation/editing (tests + UX polish)
- ⭐ Review polish (average rating display, validation states)
- 🧾 Watchlist & Favorites
-  Watchlist: allowed when no available showtime 
- Favorites: allowed after user attended a showtime (in progress)
- ⭐ Service review (post-showtime only)
- ✉️ Email confirmation 
- 💳 Simple payment
- 📣 Notifications – Users receive a notification after every major action (booking, review, payment, etc.).
 ## 🏗️ Next Up

- 🐳 Docker & CI/CD (Compose, build/test/workflow)

- 🎨 Frontend polish (filter panel UX, mobile tweaks, infinite scroll)

- More advanced payment logic

- VIP showtime logic

- Multi-language support

- Dark mode toggle

- Push notifications (new releases)

- Retro movie voting system

- “Coming Soon” opt-in


# 🧪 Testing

✅ Django unit tests (models, views)

✅ DRF API tests (bookings, movies, auth, etc.)

🧪 Jest unit tests for React components (planned)

⚙️ GitHub Actions CI (planned)

# 📸 Screenshots
## All Movies List Page

<img width="1886" height="875" alt="image" src="https://github.com/user-attachments/assets/f21aa082-7397-4319-af30-df42a495530d" />

## Movie Datails Page

<img width="667" height="799" alt="image" src="https://github.com/user-attachments/assets/ba31af31-77b2-4136-b579-e821280c711f" />

## Available Showtime List Page 

<img width="1914" height="885" alt="image" src="https://github.com/user-attachments/assets/41150828-909d-4c21-a8b4-1712b4463ec2" />

## User Bookings Page

<img width="651" height="747" alt="image" src="https://github.com/user-attachments/assets/a213987c-c138-4dd7-b1c2-9f0febe99b42" />

## Booking Confirmed (Payed)

<img width="741" height="450" alt="image" src="https://github.com/user-attachments/assets/4fd705df-2716-4fcf-9574-7153dd59a67c" />

## Booking In Progress

<img width="741" height="491" alt="image" src="https://github.com/user-attachments/assets/d9e31bde-0cdf-4f7d-8fc9-46d08dc7ed37" />

## Booking Canceled


<img width="745" height="473" alt="image" src="https://github.com/user-attachments/assets/98da251e-ca40-4096-908f-e126df830f61" />




