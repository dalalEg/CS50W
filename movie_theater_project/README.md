🎬 Movie Theater Web App

A full-stack web application for booking movie tickets — featuring dynamic seat selection, user reviews, rich search & filtering, and an admin management system. Built with Django REST Framework and React.

⚠️ Actively developed – frontend and backend integration in progress.

# 🛠 Features

- 🎟️ Showtime-based seat selection with a visual seat picker

- 🔐 User authentication (register / login / logout)

- 🧾 Booking system with automatic user linking + confirmation view

- ⭐ Reviews & ratings (edit/delete, anonymous option)

- 🔍 Powerful search & filters (title/keyword, genre, rating, year, duration, theater)

- 🎬 Movie browsing with trailers, posters, and credits

- 👤 User profile with booking history & reviews

- 🏛️ Theaters & auditoriums directory

- 🛠️ Admin panel for movies, showtimes, actors, directors, producers, etc.

- 🐳 Dockerized (in progress)

- ⚙️ CI/CD with GitHub Actions (in progress)

- 🔔 Coming soon notifications (planned)

- 🗳️ Retro request voting system (planned)

# 📦 Tech Stack

- Backend: Django + Django REST Framework

- Frontend: React + Axios + React Router + Bootstrap

- Database: PostgreSQL

- Auth: Django sessions

- DevOps: Docker, GitHub Actions

- Media: ImageField (poster), URLField (trailer)

- Planned: Stripe integration for payments

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

- 🧹 Clean Theater ↔ Auditorium relationship

- 🎥 Movie Detail page (trailer, actors, reviews, showtimes)

- 🪑 Showtime detail with visual seat map

- 🏛️ Our Theaters page (theaters & auditoriums)

- 🧾 Booking logic + confirmation UI (click-through to details)

- ⭐ Review system (with edit/delete and anonymous toggle)

- 🛒 End-to-end booking flow (showtime → seats → confirmation)

- ➕ Detail pages: Directors, Actors, Producers, Theaters

- 🔍 Search & filters for movies/showtimes/theaters
-  (genre, rating, year, duration, sort, keyword)

- 👤 Polished profile UI (bookings, reviews)

 ## 🏗️ Next Up

- 🗑️ Booking cancellation/editing (tests + UX polish)

- ⭐ Review polish (average rating display, validation states)

- 🧾 Watchlist & Favorites

- - Watchlist: allowed when no available showtime

- - Favorites: allowed after user attended a showtime

- ✉️ Optional email confirmation for registration

- 💳 Stripe payment integration

- 📣 Notifications (watchlist alerts, review replies)

- 🐳 Docker & CI/CD (Compose, build/test/workflow)

- 🎨 Frontend polish (filter panel UX, mobile tweaks, infinite scroll)

## 🧩 Backlog / Ideas

- VIP showtime logic

- Multi-language support

- Dark mode toggle

- Push notifications (new releases)

- Retro movie voting system

- “Coming Soon” opt-in

- Watchlist / favorites expansions

- DevOps: full CI pipeline with tests, linting & formatting rules

# 🧪 Testing

✅ Django unit tests (models, views)

✅ DRF API tests (bookings, movies, auth, etc.)

🧪 Jest unit tests for React components (planned)

⚙️ GitHub Actions CI (planned)

# 📸 Screenshots
<img width="1886" height="875" alt="image" src="https://github.com/user-attachments/assets/f21aa082-7397-4319-af30-df42a495530d" /> <img width="667" height="799" alt="image" src="https://github.com/user-attachments/assets/ba31af31-77b2-4136-b579-e821280c711f" /> <img width="1914" height="885" alt="image" src="https://github.com/user-attachments/assets/41150828-909d-4c21-a8b4-1712b4463ec2" />
