# 🎬 Movie Theater Web App

[![CI](https://github.com/dalalEg/CS50W/actions/workflows/ci.yml/badge.svg)](https://github.com/dalalEg/CS50W/actions/workflows/main.yml)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-blue.svg)](https://flake8.pycqa.org/)
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen.svg)](91%)

A full-stack movie theater booking web application built with Django REST Framework and React, featuring real-time seat selection, user reviews, watchlists, search & filtering, notifications, and an admin management system.

✅ Backend deployed on Render with PostgreSQL
✅ Frontend deployed on Netlify

## 🛠 Features

* 🔐 **User Authentication** – Register, login, logout with secure sessions ✅
* 🎬 **Movie Browsing** – Trailers, posters, credits, rich details ✅
* 🎟️ **Seat Selection** – Interactive seat map per showtime (seats stored per showtime) ✅
* 🧾 **Booking System** – Create/confirm/cancel; seat-level reservation integrity ✅
* ⭐ **Movie Reviews** – Write/edit/delete, average rating display ✅
* ⭐ **Service Reviews** – (post-showtime only) ✅
* 📌 **Watchlist & Favorites** – ✅ implemented
* 📣 **In-App Notifications (Celery)** – Pending payment reminder, auto-cancel unpaid bookings, showtime reminder, new showtime alert ✅
* 💳 **Payments** – Simple checkout flow (mock) ✅
* 🏛️ **Theaters & Auditoriums** – Venue directory ✅
* 🛠️ **Admin Panel + Analytics** – KPI dashboard (users, bookings, revenue, top movies, watchlist), auditorium utilization ✅
* 🐳 **Dockerized Setup** – Compose for backend/frontend/DB/Redis ✅
* ⚙️ **CI/CD with GitHub Actions** – Lint, test, build, deploy 🔄 in progress
* 🌙 **Dark Mode Toggle** – 🔄 planned
* 🗳️ **Feature Voting** – 🔄 planned

## 🛠️ Tech Stack

* **Backend:** Django + DRF, PostgreSQL(currently using SQLite), Celery + Redis
* **Frontend:** React, Axios, React Router, Bootstrap
* **Auth:** Django sessions + CSRF
* **Deployment:** Render (backend + DB), Netlify (frontend)
* **Containerization:** Docker Compose
* **CI/CD:** GitHub Actions – Python/Node jobs, lint, tests, coverage

## 🚧 Roadmap

### ✅ Done

* Full backend models & migrations (Movie, Seat, Showtime, Booking, Actor, Director, Producer, Theater, Auditorium)
* Seeded test data (genres, movies, theaters)
* REST API with DRF
* Auth: login/register/logout (Django backend + React frontend)
* List all movies, show available showtimes
* Profile API (authenticated user)
* Actor/Director/Genre/Producer management via API
* React app setup (routing, Axios, proxy)
* Frontend ↔ Backend integration
* Mobile-responsive layout (Bootstrap)
* Movie Detail page (trailer, actors, reviews, showtimes)
* Showtime detail with visual seat map
* Booking flow (seat selection → confirmation)
* Review system (edit/delete, average rating)
* Watchlist & Favorites logic
* Service review (post-showtime only)
* Email confirmation & notifications (Celery tasks)
* Admin analytics (users/bookings/revenue/top movies/watchlist + auditorium utilization)
* Dockerized Compose setup

### 🚧 Next Up

* ⚙️ CI/CD (GitHub Actions) – Python/Node job matrix, migrations, fixtures, test reports, Docker build & push
* 🎨 Frontend polish – Filter UX, mobile refinements, infinite scroll/pagination
* 💳 Payments – Refunds, promo codes, VIP pricing tiers
* 🎟️ VIP showtime logic – Actor events, limited seats, dynamic pricing
* 🌍 i18n – Multi-language support
* 🗳️ Feature voting & retro/classic screenings
* 🌙 Dark mode toggle

## 🧪 Testing

* ✅ Django tests: models, viewsets, API (bookings, movies, auth, reviews)
* ✅ Seat/booking integrity: seat reservation & double-booking prevention
* ✅ Celery task tests (unit & integration with Redis)
* 🧪 React component tests (Jest + RTL) — in progress

### Running Tests & Coverage

**Backend (Django + DRF)**

```bash
# Inside the backend container
python manage.py test

# Run coverage
coverage run --source='.' manage.py test
coverage report -m
```

## 🐳 Docker Notes

* Backend, frontend, PostgreSQL, and Redis each run in separate containers
* Docker volumes persist database data (postgres\_data)
* Docker network ensures seamless service communication

## 🏗 Getting Started

### Prerequisites

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Run the project locally

```bash
# Clone the repository
git clone https://github.com/dalalEg/CS50W.git

cd movie_theater_project
# Start all services with Docker Compose
docker compose up --build
```

* Backend: [http://localhost:8000](http://localhost:8000)
* Frontend: [http://localhost:3000](http://localhost:3000)

### Live Deployment

* Frontend: [https://dali-movie-theater.netlify.app](https://dali-movie-theater.netlify.app)
* Backend API: [https://movie-theater-dots.onrender.com](https://movie-theater-dots.onrender.com)

## 🏗️ Architecture

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




---

**Note:** README reflects live deployments and current feature status as of September 2025.

# 📸 Screenshots
* All Movies List Page

<img width="1886" height="875" alt="image" src="https://github.com/user-attachments/assets/f21aa082-7397-4319-af30-df42a495530d" />

* Movie Details Page

<img width="667" height="799" alt="image" src="https://github.com/user-attachments/assets/ba31af31-77b2-4136-b579-e821280c711f" />

* Available Showtime List Page

<img width="1914" height="885" alt="image" src="https://github.com/user-attachments/assets/41150828-909d-4c21-a8b4-1712b4463ec2" />

* User Bookings Page

<img width="651" height="747" alt="image" src="https://github.com/user-attachments/assets/a213987c-c138-4dd7-b1c2-9f0febe99b42" />

* Booking Confirmed, In Progress, Canceled

<img width="741" height="450" alt="image" src="https://github.com/user-attachments/assets/4fd705df-2716-4fcf-9574-7153dd59a67c" />

* In Progress

<img width="741" height="491" alt="image" src="https://github.com/user-attachments/assets/d9e31bde-0cdf-4f7d-8fc9-46d08dc7ed37" />

* Booking Canceled


<img width="745" height="473" alt="image" src="https://github.com/user-attachments/assets/98da251e-ca40-4096-908f-e126df830f61" />




