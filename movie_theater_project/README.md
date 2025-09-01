🎬 Movie Theater Web App

A full-stack movie theater booking web application built with Django REST Framework and React, featuring real-time seat selection, user reviews, watchlists, rich search and filtering, notifications, and an admin management system for movies and showtimes

⚠️ Actively developed – frontend and backend integration in progress.

## 🛠 Features
- 🔐 **User Authentication** – Register, login, logout with secure sessions.  
- 🔍 **Advanced Search & Filters** – Title, genre, rating, year, duration, theater; sort + keyword.  
- 🎬 **Movie Browsing** – Trailers, posters, credits, rich details.  
- 🎟️ **Seat Selection** – Interactive seat map per showtime (seats stored per showtime).  
- 🧾 **Booking System** – Create/confirm/cancel; seat-level reservation integrity.  
- ⭐ **Movie Reviews** – Write/edit/delete, average rating display.  
- ⭐ **Service Reviews** – Post-showtime service ratings.  
- 📌 **Watchlist & Favorites** –  
  - Watchlist.  
  - Favorites after attending a screening.  
- 📣 **In-App Notifications (Celery)** –  
  - Pending payment reminder **T+24h**.  
  - Auto-cancel unpaid bookings **T+48h**.  
  - Showtime reminder **24h before start**.
  - **New showtime alert**: if a movie in a user’s **watchlist/favorites** gets a new showtime, notify them.  
- 👤 **User Profile** – Bookings, reviews, watchlist/favorites.  
- 🏛️ **Theaters & Auditoriums** – Venue directory.  
- 🛠️ **Admin Panel + Analytics** – KPI dashboard (users, bookings, revenue, top movies, watchlist), auditorium utilization, growth trend.  
- ✉️ **Email Confirmations** – Without email confirmation operation are limitted 
- 💳 **Payments** – Simple checkout flow (mock).  
- 🐳 **Dockerized Setup** – Compose for backend/frontend/DB (**in progress**).  
- ⚙️ **CI/CD with GitHub Actions** – Lint, test, build, deploy (**in progress**).  
- 🔔 **Coming Soon Alerts** (**planned**).  
- 🗳️ **Feature Voting** (**planned**).


## 🛠️ Tech Stack
- **Backend:** Django + DRF, Celery + Redis (scheduled tasks), PostgreSQL  
- **Frontend:** React, Axios, React Router, Bootstrap  
- **Auth:** Django sessions  
- **Background jobs:** Celery Beat for reminders & auto-cleanup  
- **Containerization:** Docker Compose (backend, frontend, db, redis)  
- **CI/CD:** GitHub Actions for automated tests & coverage  — *in progress*  
- **Media:** Posters/images served in Docker env  

---

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
-  **Celery tasks**: pending-payment reminder (T+24h), auto-delete unpaid (T+48h), 24h pre-showtime reminder ,  New showtime alert
 
- **Admin Analytics API**: users/bookings/revenue/top movies/watchlist + **auditorium utilization (seat-based)**  
- 🐳 **Dockerization** – Compose services (web, api, db, redis, worker, beat) + `.env`  

## 🚧 Roadmap → 🏗️ Next Up
- ⚙️ **CI/CD (GitHub Actions)** – Python/Node job matrix, migrations, fixtures, test reports, Docker build & push  
- 🎨 **Frontend polish** – Filter UX, mobile refinements, infinite scroll/pagination  
- 💳 **Payments** – Refunds, promo codes, VIP pricing tiers  
- 🎟️ **VIP showtime logic** – Per-auditorium/row dynamic pricing & flags  
- 🌍 **i18n** – Multi-language support  
- 🌙 **Dark mode** toggle  
- 🗳️ **Feature voting** for retro/classic screenings  
- 🎞️ **Coming Soon subscriptions** & announcements  

---

## 🧪 Testing
- ✅ **Django tests**: models, viewsets, API (bookings, movies, auth, reviews)  
- ✅ **Seat/booking integrity**: seat reservation & double-booking prevention  
- ✅ **Celery task tests** (unit): pending-reminder, auto-cancel, showtime-reminder  
- ✅ **Celery integration tests** (with Redis broker, time windows) 
- 🧪 **React component tests** (Jest + RTL) — *planned*  
- ⚙️ **CI (Actions)**: run Python/Node tests, lint, coverage gates — *planned*
## ✅ Running Tests & Coverage
```bash
# Inside the backend container
python manage.py test

# Run coverage
coverage run --source='.' manage.py test
coverage report -m
```
- Coverage: ~91% of backend code

- Ensures critical functionality works before deployment
## ⚡ Celery & Redis

- Background task processing powered by Celery

- Redis used as the task broker and result backend

- Tasks include sending reminders and notifications for bookings

- Celery worker runs automatically in the Docker container

## 🐳 Docker Notes

- Backend, frontend, PostgreSQL, and Redis each run in separate containers

- Docker volumes persist database data (postgres_data)

- Docker network ensures all services can communicate seamlessly

## 📈 CI/CD

- GitHub Actions used for automated testing, linting, and coverage reporting

- Ensures code quality and reliability for production

## 📝 Future Features

- VIP Showtime Logic: Actor events, limited seats, dynamic pricing

- Retro Voting & Review Analytics: Users vote for past shows and rate experiences
## 🏗 Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started)  
- [Docker Compose](https://docs.docker.com/compose/install/)  

### Run the project
```bash
# Clone the repository
git clone https://github.com/dalalEg/CS50W.git

cd movie_theater_project
# Start all services with Docker Compose
docker compose up --build
```
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
## 🏗️ Architecture

The system follows a **modular service-oriented architecture**:  

```plaintext
          ┌───────────────┐
          │   React UI    │
          │ (Axios + JWT) │
          └───────▲───────┘
                  │ REST API calls
                  ▼
        ┌────────────────────┐
        │   Django + DRF     │
        │  Auth, Movies,     │
        │  Bookings, Reviews │
        └───────┬────────────┘
                │
                │ Celery tasks (async jobs)
                ▼
        ┌────────────────────┐
        │   Celery Workers   │
        │ (background jobs)  │
        └───────┬────────────┘
                │
                ▼
         ┌────────────┐
         │   Redis     │
         │   Broker    │
         └────────────┘

        ┌────────────┐
        │PostgreSQL  │
        │ Relational │
        │ Database   │
        └────────────┘

```

# 📸 Screenshots
## All Movies List Page

<img width="1886" height="875" alt="image" src="https://github.com/user-attachments/assets/f21aa082-7397-4319-af30-df42a495530d" />

## Movie Details Page

<img width="667" height="799" alt="image" src="https://github.com/user-attachments/assets/ba31af31-77b2-4136-b579-e821280c711f" />

## Available Showtime List Page 

<img width="1914" height="885" alt="image" src="https://github.com/user-attachments/assets/41150828-909d-4c21-a8b4-1712b4463ec2" />

## User Bookings Page

<img width="651" height="747" alt="image" src="https://github.com/user-attachments/assets/a213987c-c138-4dd7-b1c2-9f0febe99b42" />

## Booking Confirmed (Paid)

<img width="741" height="450" alt="image" src="https://github.com/user-attachments/assets/4fd705df-2716-4fcf-9574-7153dd59a67c" />

## Booking In Progress

<img width="741" height="491" alt="image" src="https://github.com/user-attachments/assets/d9e31bde-0cdf-4f7d-8fc9-46d08dc7ed37" />

## Booking Canceled


<img width="745" height="473" alt="image" src="https://github.com/user-attachments/assets/98da251e-ca40-4096-908f-e126df830f61" />




