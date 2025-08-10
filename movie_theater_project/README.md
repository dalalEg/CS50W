# 🎬 Movie Theater Web App

A full-stack web application for booking movie tickets — featuring dynamic seat selection, user reviews, showtime filtering, and an admin management system. Built with Django REST Framework and React.

> ⚠️ Actively developed – frontend and backend integration in progress.

---

## 🛠 Features

- 🎟️ Showtime-based seat selection
- 🔐 User authentication (register/login/logout)
- 🧾 Booking system with automatic user linking
- ⭐ User ratings and reviews
- 🎬 Movie browsing with filtering (genres, showtimes)
- 👤 User profile with booking history
- 🛠️ Admin panel for movies, showtimes, actors, etc.
- 📽️ Trailers and poster support
- 🔔 Coming soon notifications (planned)
- 🗳️ Retro request voting system (planned)
- 🐳 Dockerized (in progress)
- ⚙️ CI/CD with GitHub Actions (in progress)

---

## 📦 Tech Stack

- **Backend**: Django + Django REST Framework  
- **Frontend**: React + Axios + React Router + Bootstrap  
- **Database**: PostgreSQL  
- **Authentication**: Django sessions  
- **DevOps**: Docker, GitHub Actions  
- **Media**: ImageField (poster), URLField (trailer)  
- **Planned**: Stripe integration for payments

---

## 🚧 Roadmap

### ✅ Done

- 🎯 Defined feature set and roadmap
- 🧱 Designed DB schema (Movie, Seat, Showtime, Booking, Actor, Director, etc.)
- 🔧 Implemented Django models + migrations
- 👩‍💻 Seeded test data (genres, movies, theaters)
- 🔌 Built REST API with Django REST Framework
- 🔐 Login/Register/Logout via Django backend + React frontend
- 🎞️ Display all movies
- 📅 Display available showtimes (only future ones for users)
- 👤 Profile API for authenticated user
- 🎭 Actor/Director/Genre management via API
- 🏗️ Setup React project with routing and Axios
- 🔗 Connected React to Django via proxy
- 💻 Mobile-responsive layout (Bootstrap)
- 🧹 Cleaned up Theater ↔ Auditorium relationship
- 🎥 Movie Detail Page (trailer, actors, reviews, showtimes)
- 🪑 Showtime detail page with visual seat selection
- 🏛️ Our Theaters” page with list of theaters and auditoriums
- 🧾 Booking logic + confirmation page
- ⭐ Review system 
- 🧾 Booking confirmation UI
- 🛒 Booking flow (showtime → seats → confirmation)
- ➕ Added pages for viewing Directors, Actors, Producers, and Theater details


---

### 🏗️ In Progress

- 👤 Profile page UI
- 🐳 Docker setup
- 🔧 GitHub Actions for CI

---

### 🧩 Backlog / Ideas

#### Features

- Add star-based rating system  
- VIP showtime logic  
- Multi-language support  
- Dark mode toggle  
- Push notifications (new releases)

#### Booking & Payments

- Stripe integration  
- Add payment confirmation  
- Handle booking cancellation/editing  
- Implement visual seat picker  

#### Engagement

- Retro movie voting system  
- “Coming Soon” notification opt-in  
- Watchlist / favorites  

#### DevOps

- Docker Compose for full stack  
- CI pipeline with full tests  
- Linting + code formatting rules  

---

## 🧪 Testing

- ✅ Django unit tests for models and views (in progress)
- ✅ DRF API tests (bookings, movies, auth, etc.)
- 🧪 Jest unit tests for React components (planned)
- ⚙️ GitHub Actions integration for CI pipeline (planned)

---

## 📸 Screenshots
<img width="1910" height="896" alt="image" src="https://github.com/user-attachments/assets/def53204-ce69-4559-ad9b-61db2bc449bd" />

<img width="667" height="799" alt="image" src="https://github.com/user-attachments/assets/ba31af31-77b2-4136-b579-e821280c711f" />


