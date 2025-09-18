# 🎬 Movie Theater Web App

[![CI](https://github.com/dalalEg/CS50W/actions/workflows/ci.yml/badge.svg)](https://github.com/dalalEg/CS50W/actions/workflows/main.yml)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-blue.svg)](https://flake8.pycqa.org/)
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen.svg)](91%)

A **full-stack movie theater booking platform** built with **Django REST Framework + React**, featuring **real-time seat selection, bookings, reviews, watchlists, notifications, and admin analytics**.  

🌐 **Live Demo:**  
- Frontend → [Netlify Deployment](https://dali-movie-theater.netlify.app)  
- Backend API → [Render Deployment](https://movie-theater-dots.onrender.com)  

---

## ✨ Highlights

- 🔐 **User Authentication** – Secure sessions (register, login, logout)  
- 🎬 **Movie Browsing** – Trailers, posters, credits, details  
- 🎟️ **Interactive Seat Selection** – Seat-level reservation integrity  
- 🧾 **Booking Flow** – Create/confirm/cancel bookings  
- ⭐ **Movie & Service Reviews** – Post-showtime feedback, ratings  
- 📌 **Watchlist & Favorites** – Personalized movie tracking  
- 📣 **Notifications (Celery)** – Reminders, cancellations, new showtimes  
- 💳 **Mock Payments** – Checkout simulation  
- 🏛️ **Theater & Auditoriums** – Venue + seating structure  
- 📊 **Admin Dashboard** – KPIs: users, bookings, revenue, utilization  
- 🐳 **Dockerized Setup** – Backend, frontend, DB, Redis  
- ⚙️ **CI/CD (GitHub Actions)** – Linting, tests, build, deploy  

---

## 🖼 Screenshots

**Movies List Page**  
<img width="1886" alt="movies-list" src="https://github.com/user-attachments/assets/f21aa082-7397-4319-af30-df42a495530d" />

**Movie Details Page**  
<img width="667" alt="movie-details" src="https://github.com/user-attachments/assets/ba31af31-77b2-4136-b579-e821280c711f" />

**Available Showtime List**  
<img width="1914" alt="showtime-list" src="https://github.com/user-attachments/assets/41150828-909d-4c21-a8b4-1712b4463ec2" />

**User Bookings Page**  
<img width="651" alt="user-bookings" src="https://github.com/user-attachments/assets/a213987c-c138-4dd7-b1c2-9f0febe99b42" />

**Booking Status (Confirmed, In Progress, Canceled)**  
<img width="741" alt="booking-status" src="https://github.com/user-attachments/assets/4fd705df-2716-4fcf-9574-7153dd59a67c" />
<img width="741" alt="booking-in-progress" src="https://github.com/user-attachments/assets/d9e31bde-0cdf-4f7d-8fc9-46d08dc7ed37" />
<img width="745" alt="booking-canceled" src="https://github.com/user-attachments/assets/98da251e-ca40-4096-908f-e126df830f61" />

---

## 🛠 Tech Stack

**Backend** → Django + DRF, PostgreSQL (SQLite for local dev), Celery + Redis  
**Frontend** → React, Axios, React Router, Bootstrap  
**Auth** → Django sessions + CSRF  
**Deployment** → Render (backend + DB), Netlify (frontend)  
**Containerization** → Docker Compose (backend, frontend, DB, Redis)  
**CI/CD** → GitHub Actions (Python/Node jobs, lint, tests, coverage, deploy)  

---

## 🧪 Testing

- ✅ Django tests for models, viewsets, API (bookings, movies, auth, reviews)  
- ✅ Seat/booking integrity → prevents double booking  
- ✅ Celery task tests (unit + integration with Redis)  
- 🧪 React component tests (Jest + RTL) — *in progress*  

Run tests:

```bash
# Inside backend container
python manage.py test
```
# Coverage
coverage run --source='.' manage.py test
coverage report -m

# Running Locally (Docker)
Prerequisites:

Docker https://www.docker.com/get-started

Docker Compose https://docs.docker.com/compose/install/

Setup:
```bash
# Clone the repository
git clone https://github.com/dalalEg/CS50W.git
cd movie_theater_project
# Build + run services
docker compose up --build
``` 

Backend → http://localhost:8000

Frontend → http://localhost:3000

# 🏗 Architecture
          ┌───────────────┐
          │   React UI    │
          │ (Axios + CSRF)│
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
        │ (notifications)    │
        └───────┬────────────┘
                │
                ▼
         ┌────────────┐
         │   Redis    │
         │   Broker   │
         └────────────┘

        ┌────────────┐
        │ PostgreSQL │
        │ Database   │
        └────────────┘


# 📌 Note: Project reflects live deployments and feature set as of September 2025.
