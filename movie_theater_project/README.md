# 🎬 Movie Theater Booking System
[![CI](https://github.com/dalalEg/CS50W/actions/workflows/ci.yml/badge.svg)](https://github.com/dalalEg/CS50W/actions/workflows/main.yml)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-blue.svg)](https://flake8.pycqa.org/)
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen)](https://app.codecov.io/github/dalaleg/cs50w/commit/a813473c1eff840644d0a2a24b94942094a752d2)

A **full-stack web application** for browsing movies, selecting showtimes, choosing seats, and making bookings.  
The system integrates **Django REST Framework** on the backend with a **React frontend**, and stores data in **PostgreSQL**.  
It provides a modern, mobile-friendly interface and is designed to simulate a realistic theater booking flow.

🌐 **Live Demo:**  
- Frontend → [Netlify Deployment](https://dali-movie-theater.netlify.app)  
- Backend API → [Render Deployment](https://movie-theater-dots.onrender.com)  
- Demo Video → [YouTube Walkthrough](https://www.youtube.com/watch?v=YrqwYAZTVQ8)
---

## 🚀 Project Overview

This project replicates the core features of a real-world movie theater platform. Users can register, log in, browse available movies, check showtimes, select seats in real time, and confirm or cancel bookings. Additional features include **reviews, watchlists, notifications, and an analytics dashboard for admins**.  

From the start, the project was designed to go beyond earlier CS50W assignments. Unlike the commerce or social network projects, this system focuses on **scheduling and seat-level booking integrity**, which required careful API design, state management, and real-time validation.

The stack also incorporates **Celery with Redis for background tasks** (e.g., sending booking notifications), **Docker Compose for containerization**, and **GitHub Actions for CI/CD**, making the system robust, scalable, and production-ready.

---

## ✨ Features

- **User Authentication**
  - Register, log in, and log out with Django sessions and CSRF protection.
  - Secure access to bookings and profiles.

- **Movies and Showtimes**
  - Browse movies with details like title, description, runtime, posters, and trailers.
  - View showtimes by date, time, available seats, language, and auditorium.
  - Advanced search and filtering by title, genre, release date, or showtime.

- **Seat Selection and Booking**
  - Interactive seat maps with real-time availability checks.
  - Server-side validation to prevent double-booking.
  - Full booking flow: confirmation, cancellation, and payment simulation.

- **User Dashboard**
  - Manage bookings, reviews, and watchlists.
  - Update or cancel bookings as allowed.
  - Add/remove movies from watchlists and favorites.
  - Create, edit, or delete reviews; rate service post-showtime.
- **News Section**
  - Announcements for upcoming movies, releases, and events.

- **Admin Features**
  - Django Admin for managing movies, showtimes, and bookings.
  - Dashboard with KPIs: revenue, utilization, users, and bookings.
  - Role-based permissions (e.g., users edit only their reviews).

- **Notifications & Background Tasks**
  - Signals trigger notifications for watchlist updates or favorite releases.
  - Celery tasks handle reminders, pending booking alerts, unpaid cancellations, and post-showtime feedback.

- **Responsive Design**
  - Optimized for desktops, tablets, and mobile devices.

---

## 🛠️ Distinctiveness and Complexity

This project is **distinct** from other CS50W assignments in both concept and implementation.  

It is **not a social network** (like Project 4), since it focuses on theater operations, scheduling, and ticketing rather than user relationships (users can't see other users' activities).  
It is **not an e-commerce site** (like Project 2), since it doesn’t use a shopping cart model; instead, it handles real-time seat maps, showtime scheduling, and validation for bookings—closer to airline/train reservation systems than to product checkout flows.  

In terms of **complexity**, the project required solving challenges beyond earlier projects:
- **Frontend + Backend Integration:** React for interactive UI, Django REST Framework for APIs.  
- **Real-Time Seat Validation:** Concurrency-safe checks to prevent race conditions.  
- **Asynchronous Tasks:** Celery for notifications and background processes.  
- **Interconnected Models:** Complex schema for Movies, Showtimes, Bookings, Users, Reviews, etc.  
- **Scalability:** Dockerized setup, CI/CD pipeline, and cloud deployment.  

These elements ensure the project is not only distinct from the course’s prior projects but also reflects real-world engineering complexity.

---

## 🛠 Tech Stack

**Backend** → Django + DRF, PostgreSQL (SQLite for local dev), Celery + Redis  
**Frontend** → React, Axios, React Router, Bootstrap  
**Auth** → Django sessions + CSRF  
**Deployment** → Render (backend + DB), Netlify (frontend)  
**Containerization** → Docker Compose (backend, frontend, DB, Redis)  
**CI/CD** → GitHub Actions (Python/Node jobs, lint, tests, coverage, deploy)  

---

## 📂 File Structure
- **/movie-theater-project**
    - **/backend**
        - **/management** → Main Django app
            - `admin.py` → Registers models for the Django admin interface for easy management of movies, showtimes, and bookings.
            - `app.py` → Connects signal handlers on app startup.
            - `models.py` → Database models (Movie, Showtime, Booking, Review, Watchlist, Auditorium, etc.).
            - `permissions.py` → Implements fine-grained access control, such as allowing only the review author to edit their review.
            - `views.py` & `serializers.py` → Defines REST API endpoints and serializes data for frontend consumption.
            - `signals.py` → Contains Django post_save signals that automatically create notifications when new showtimes are added or when favorite directors/producers release new movies.
            - `tasks.py` → Implements Celery asynchronous tasks for: Sending upcoming showtime reminders, Notifying users of pending bookings, Automatically canceling unpaid bookings and freeing seats, Updating booking statuses after showtimes to mark attendance and send feedback reminders.
            - `test_models.py` → Unit tests for models.
            - `tests/` → Unit tests for bookings, authentication, and seat integrity.
            - `urls.py` → API routing for all endpoints in the management app.
        - **/media**
            - **/posters** → Stores movie poster images used in the app. Only committed poster assets are included; user-uploaded content is ignored in the repository.
        - **/movie_theater**
            - `celery.py` → Celery application setup for asynchronous tasks.
            - `settings.py` → Django configuration including database connections, installed apps, middleware, and static/media settings.
        - `Dockerfile` → Container configuration for backend services.
        - `manage.py` → Django CLI entry point for migrations, running the server, and administrative tasks.
        - `requirements.txt` → Lists all Python dependencies needed for backend functionality, including Django, DRF, Celery, Redis, and others.
        - ## ⚠️ Notes
          Local database & ignored files: `db.sqlite3` and Celery runtime files (`celerybeat-schedule.*`) are kept locally and are not committed. Sample data exports (`db.json`, `prod_data.json`) may be included to demonstrate current showtimes and for testing purposes.
    - **/movie-theater-frontend**
        - `src/api/` → Handles all HTTP requests to the backend API (movies, showtimes, bookings, reviews, notifications).
        - `src/components/` → Reusable React components, including:
            - MovieList – Displays all movies with advanced search & filter.
            - ShowtimeDetail – Shows showtime info and seat map.
        - `src/contexts/` → Authentication context and global state management (user session, watchlist, favorites, notifications).
        - `src/styles/` → CSS/SCSS files for responsive layout, mobile-friendly UI, and component styling.
        - `src/tests/` → Jest and React Testing Library tests for critical components and UI interactions.
        - `src/App.js` → Main React entry point, sets up routes, providers, and application layout.
        - `src/index.js` → Wraps App with context providers and renders the React app.
        - `package.json` → Frontend dependencies and scripts for development, testing, and build.
        - `setupTests.js` → Configures Jest and React Testing Library for frontend testing.
        - `.babelrc` → Babel configuration for JavaScript transpilation.
        - `jest.config.js` → Jest configuration for unit and integration tests.
        - `Dockerfile` → Defines frontend container for deployment.
    - **/posters/** → Contains static assets such as movie posters used in the frontend UI.
    - **/.env.local/** → (not shared in repo) Local environment variables for development. This file is not pushed to GitHub for security reasons, but it is required when running the project locally.
    - **/.env.production** → (not shared in repo) Production environment variables (e.g., database credentials, API keys). This file is also excluded from GitHub for security reasons, but is required when deploying the project.
    - **/docker-compose.yml** → Multi-service configuration file that defines the setup for backend, frontend, PostgreSQL, Redis, and Celery workers.
    - **/README.md** → Project documentation (this file).

---

## ▶️ How to Run Locally

### 🚀 Quick Start (Docker)
Prerequisites: [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/).

```bash
# Clone the repository
git clone https://github.com/dalalEg/CS50W.git
cd movie_theater_project

# Build and run all services
docker compose up --build
```
- Backend → http://localhost:8000
- Frontend → http://localhost:3000
### Manual Setup
1. Clone the repository
```bash
git clone https://github.com/dalalEg/CS50W.git
cd movie_theater_project
```
2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # (or venv\Scripts\activate on Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
    - Backend will run at: http://127.0.0.1:8000/
3.Frontend setup
```bash
cd ../movie-theater-frontend
npm install
npm start
```

## 📦 Requirements
All backend dependencies are listed in requirements.txt.
Frontend dependencies are listed in frontend/package.json.

## 📱 Mobile Responsiveness
The application is fully responsive. Seat grids, movie cards, and booking forms adapt to smaller screens to ensure usability on mobile devices.

## 🖼 Screenshots
### Movies List Page

<img width="1904" height="887" alt="image" src="https://github.com/user-attachments/assets/0500e666-7a9d-4ead-90c1-6e9b267f6c66" />

### Movie Details Page

<img width="498" height="809" alt="image" src="https://github.com/user-attachments/assets/452427b3-c043-4b9e-aaac-a48163bcd980" />

### Movie Reviews Page

<img width="1904" height="890" alt="image" src="https://github.com/user-attachments/assets/4925f12b-4ec7-477e-93c1-116746bb0323" />

### Available Showtime List

<img width="1918" height="894" alt="image" src="https://github.com/user-attachments/assets/95ed4923-92e2-4d5b-92cc-3a62447a96b2" />

### Showtime datails

<img width="1276" height="898" alt="image" src="https://github.com/user-attachments/assets/c17445e8-2d7b-45bc-9a64-6671b67e0473" />


### User Bookings Page

<img width="651" alt="user-bookings" src="https://github.com/user-attachments/assets/a213987c-c138-4dd7-b1c2-9f0febe99b42" />

### Booking Status (Confirmed, In Progress, Canceled)
<img width="741" alt="booking-in-progress" src="https://github.com/user-attachments/assets/d9e31bde-0cdf-4f7d-8fc9-46d08dc7ed37" />

### Latest News Page 

<img width="1919" height="897" alt="image" src="https://github.com/user-attachments/assets/ebd0b028-59b9-4e41-97cd-8cdb81921ab0" />

## 🧪 Testing
Django tests for models, viewsets, API (bookings, movies, auth, reviews).
Seat/booking integrity → prevents double booking.
Celery task tests (unit + integration with Redis).
### Run tests:
```bash
# Inside backend container
python manage.py test
```
### Coverage:
```bash
coverage run --source='.' manage.py test
coverage report -m
```

## 📝 Additional Notes

The project demonstrates not only full-stack coding but also design considerations for scalability and user experience.

## License: This project is licensed under the MIT License. See LICENSE for details.

## 🙌 Acknowledgments
This project was built as the final project for CS50’s Web Programming with Python and JavaScript.
It reflects my personal effort to design and implement a realistic full-stack system beyond the course’s earlier projects.

⭐ Star this repo if you find it useful, and check out the live demo to explore the features!
