# 🎬 Movie Theater Booking System

A **full-stack web application** for browsing movies, selecting showtimes, choosing seats, and making bookings. The system integrates **Django REST Framework** on the backend with a **React frontend**, and stores data in **PostgreSQL**. It provides a modern, mobile-friendly interface and is designed to simulate a realistic theater booking flow.

🌐 **Live Demo:**  
- Frontend → [Netlify Deployment](https://dali-movie-theater.netlify.app)  
- Backend API → [Render Deployment](https://movie-theater-dots.onrender.com)  
- Demo Video → [YouTube Walkthrough](https://www.youtube.com/watch?v=YrqwYAZTVQ8)

---

## 🛠️ Distinctiveness and Complexity

This project is **fundamentally distinct** from other CS50W assignments in both concept and implementation complexity.

### **Why This Is NOT a Social Network (Unlike Project 4)**

Project 4 focused on user-to-user interactions: following users, posting content, liking posts, and viewing other users' activities. My movie theater system operates on an entirely different paradigm—**business-to-consumer service booking**. Users interact with a centralized inventory system (showtimes and seats) rather than with each other. There are no user profiles to view, no following mechanisms, no feeds of user activities, and no social interactions. The core functionality revolves around **resource reservation** (seats) and **scheduling** (showtimes), which are fundamentally different from social networking concepts.

### **Why This Is NOT E-Commerce (Unlike Project 2)**

While Project 2 involved product listings and bidding, my system doesn't use a shopping cart model or product inventory management. Instead, it implements **real-time seat reservation** with time-sensitive booking windows, which is closer to airline or concert ticket systems than traditional e-commerce. The key differences include:

- **Inventory Scarcity**: Seats are unique, non-replenishable resources tied to specific time slots
- **Temporal Constraints**: Bookings become invalid after showtime, unlike products that remain available
- **Concurrency Management**: Multiple users can compete for the same seat simultaneously, requiring atomic database operations
- **Status Workflows**: Bookings progress through Pending → Confirmed → Attended states with automated transitions

### **Technical Complexity Beyond Previous Projects**

This project required solving engineering challenges not present in earlier assignments:

**1. Real-Time Concurrency Management**
- Implemented atomic seat booking with Django's `F()` expressions to prevent race conditions
- Server-side validation ensures no double-booking even under high concurrent load
- Database-level constraints maintain data integrity across simultaneous booking attempts

**2. Asynchronous Task Processing**
- Celery background tasks handle business-critical workflows: payment deadline enforcement, showtime reminders, and automatic seat release
- Redis message broker enables distributed task processing
- Implemented retry mechanisms with exponential backoff for failed notifications

**3. Complex State Management**
- Frontend React context manages authentication, notifications, and real-time seat availability
- Backend implements sophisticated booking lifecycle management with multiple status transitions
- Cross-cutting concerns like user points, watchlists, and notifications require careful state synchronization

**4. Production-Grade Architecture**
- Dockerized multi-service deployment with PostgreSQL, Redis, and Celery workers
- CI/CD pipeline with automated testing, linting, and deployment
- Environment-specific configuration management for development and production

**5. Advanced API Design**
- RESTful endpoints with custom actions for complex business operations (seat selection, booking confirmation)
- Nested resource relationships (movies→showtimes→seats→bookings) with proper filtering and pagination
- Custom serializers handle complex validation logic and nested data transformation

These technical challenges required understanding distributed systems, database concurrency, background job processing, and production deployment—concepts far beyond the scope of previous course projects.

---

## 📂 Complete File Documentation

### **Backend Files (Django)**

#### **backend/management/models.py**
This file contains the complete database schema for the movie theater system. It defines 15+ interconnected models that represent the business domain:

- **User Model**: Extends Django's AbstractUser with additional fields for `points` (loyalty system) and `email_verified` (account verification status)
- **Movie Model**: Core entity with fields for title, description, poster images, trailer URLs, duration, and rating. Includes methods for genre aggregation and string representation
- **Genre Model**: Simple classification system with many-to-many relationship to movies
- **Theater/Auditorium/Seat Hierarchy**: Three-level venue structure where Theater contains multiple Auditoriums, each containing multiple Seats with individual pricing
- **Showtime Model**: Links movies to specific auditoriums with start times. Includes critical `available_seats` field that's atomically updated during bookings. Custom save method auto-populates available seats from auditorium capacity
- **Booking Model**: Central transaction entity linking users to showtimes with seat assignments. Includes status tracking (Pending/Confirmed/Cancelled), cost calculation, and attendance marking
- **Review System**: User reviews with ratings, linked to both movies and users with timestamp tracking
- **Notification Model**: System-generated messages for users with read/unread status
- **Watchlist/Favorites**: Many-to-many through tables for user preferences
- **Actor/Director/Producer**: Personnel models with many-to-many relationships to movies through Role intermediary
- **News Model**: Admin-managed announcements with publication dates

The models implement crucial business logic including automatic cost calculation, seat availability tracking, and relationship integrity constraints.

#### **backend/management/serializers.py**
Contains Django REST Framework serializers that handle API data transformation and validation:

- **MovieSerializer**: Transforms movie objects to/from JSON with nested genre data and computed fields like average ratings
- **ShowtimeSerializer**: Includes related movie and auditorium data with real-time seat availability
- **BookingSerializer**: Most complex serializer handling seat selection validation, booking creation, and update logic. Implements custom `create()` and `update()` methods that:
  - Validate seat availability before booking
  - Atomically update seat status and showtime availability
  - Handle seat changes during booking updates (release old seats, book new ones)
  - Recalculate total cost based on selected seats
- **SeatSerializer**: Simple serializer for seat data with booking status
- **UserSerializer**: Handles user registration and profile data with password validation
- **ReviewSerializer**: Manages movie reviews with user authorization checks
- **NotificationSerializer**: Formats notification data for frontend consumption

Key validation logic includes checking seat availability, preventing past showtime bookings, and ensuring users can only modify their own bookings.

#### **backend/management/views.py**
Implements API endpoints using Django REST Framework ViewSets:

- **MovieViewSet**: Full CRUD operations for movies with custom actions for retrieving showtimes and managing watchlists. Includes filtering by genre, search by title, and ordering options
- **ShowtimeViewSet**: Manages showtime data with filtering by date and movie. Custom queryset optimization using `select_related()` for performance
- **BookingViewSet**: Handles booking lifecycle with user-specific filtering (users only see their own bookings). Implements custom permissions ensuring booking ownership
- **SeatViewSet**: Provides seat availability data with real-time status updates
- **UserViewSet**: User management with registration and profile endpoints
- **ReviewViewSet**: Movie review CRUD with user authorization
- **NotificationViewSet**: User notification management with read/unread status updates

Each ViewSet includes appropriate permission classes, filtering options, and custom business logic for complex operations like booking confirmation and cancellation.

#### **backend/management/admin.py**
Django admin interface configuration for backend data management:

- **Custom Admin Classes**: Each model has tailored admin interface with optimized list displays, search fields, and filters
- **Inline Editing**: SeatInline allows editing seats directly from showtime admin pages
- **Custom Forms**: BookingForm includes dynamic seat filtering based on selected showtime
- **Readonly Fields**: Prevents accidental modification of calculated fields like booking costs
- **Search Optimization**: Implements search across related fields (e.g., search bookings by movie title)

The admin interface provides a complete backend management system for theater staff to manage movies, showtimes, and bookings without technical knowledge.

#### **backend/management/tasks.py**
Celery asynchronous tasks for background business logic:

- **send_showtime_reminder()**: Sends notifications 24 hours before showtime starts
- **send_pending_booking_reminder()**: Alerts users about unpaid bookings approaching deadline
- **delete_unpaid_booking()**: Automatically cancels unpaid bookings after 24 hours and releases seats back to inventory
- **update_booking_status_after_showtime()**: Marks confirmed bookings as attended and sends thank you messages post-showtime

Each task includes retry logic, error handling, and database transaction safety. These tasks are critical for maintaining booking integrity and customer communication.

#### **backend/management/signals.py**
Django signal handlers for automated business logic:

- **Post-save signals**: Automatically create notifications when users add movies to watchlists or when favorite directors release new movies
- **Booking signals**: Trigger point awards and inventory updates when bookings are confirmed
- **User registration signals**: Send welcome notifications and initialize user preferences

Signals enable event-driven architecture where related data updates automatically without explicit coupling between components.

#### **backend/management/urls.py**
API routing configuration using Django REST Framework routers:

- **Router Setup**: DefaultRouter automatically generates RESTful URLs for all ViewSets
- **Custom Endpoints**: Additional paths for authentication, search, and specialized actions
- **API Versioning**: Structured for future API version management
- **Nested Resources**: Routes for related data like movie showtimes and user bookings

The URL configuration provides a clean, RESTful API surface that follows Django conventions.

#### **backend/movie_theater/settings.py**
Main Django configuration file with environment-specific settings:

- **Database Configuration**: PostgreSQL for production, SQLite for development
- **Celery Setup**: Redis broker configuration for background tasks
- **Static/Media Files**: Configuration for image uploads and static asset serving
- **CORS Settings**: Enables frontend-backend communication in development
- **Security Settings**: CSRF protection, secure headers, and authentication configuration
- **Environment Variables**: Sensitive data loaded from environment files

Settings are structured for easy deployment across development and production environments.

#### **backend/movie_theater/celery.py**
Celery application configuration for background task processing:

- **Broker Configuration**: Redis connection setup for task queuing
- **Task Discovery**: Automatic detection of task modules across Django apps
- **Beat Schedule**: Periodic task scheduling for recurring operations like reminder sending
- **Error Handling**: Dead letter queues and retry configuration

This enables the asynchronous processing crucial for booking deadlines and user notifications.

### **Frontend Files (React)**

#### **movie-theater-frontend/src/App.js**
Main React application component that orchestrates the entire frontend:

- **Routing Setup**: React Router configuration for all application pages (movies, showtimes, bookings, user dashboard)
- **Context Providers**: Wraps application in AuthContext and NotificationContext for global state management
- **Layout Structure**: Defines consistent navigation header and main content area
- **Protected Routes**: Implements route guards that redirect unauthenticated users to login
- **Error Boundaries**: Catches and handles React component errors gracefully

The App component serves as the architectural foundation, ensuring proper state management and navigation throughout the user experience.

#### **movie-theater-frontend/src/components/MovieList.js**
Comprehensive movie browsing interface with advanced filtering capabilities:

- **Pagination Logic**: Implements page-by-page movie loading with "Load More" functionality to improve performance
- **Search and Filtering**: Real-time search by title, filtering by genre, rating, duration, and release year
- **Sorting Options**: Multiple sort criteria including alphabetical, popularity, release date, and duration
- **Responsive Cards**: Movie cards that adapt to different screen sizes with poster images, ratings, and descriptions
- **Navigation Integration**: Click handlers that route to detailed movie pages
- **Loading States**: Proper loading indicators and error handling for API calls

This component demonstrates complex state management with multiple interconnected filters and real-time data fetching.

#### **movie-theater-frontend/src/components/ShowtimeDetail.js**
Interactive seat selection interface for booking process:

- **Seat Map Rendering**: Visual grid representation of auditorium seats with real-time availability status
- **Selection Logic**: Click handlers for seat selection/deselection with visual feedback
- **Booking Validation**: Client-side checks for seat availability and user authentication
- **Cost Calculation**: Real-time price updates as users select/deselect seats
- **Booking Submission**: Form handling for booking confirmation with error management
- **Responsive Design**: Seat grid adapts to mobile devices with touch-friendly interfaces

The component manages complex UI state for seat selection while maintaining synchronization with backend availability data.

#### **movie-theater-frontend/src/components/Register.js**
User registration form with comprehensive validation:

- **Form State Management**: Controlled inputs for username, email, password, and confirmation
- **Client-side Validation**: Real-time validation for password matching, email format, and required fields
- **API Integration**: Registration API calls with proper error handling and success feedback
- **Notification Integration**: Triggers welcome notifications upon successful registration
- **Navigation Logic**: Automatic redirection to appropriate pages based on registration status
- **Accessibility Features**: Proper form labels, error announcements, and keyboard navigation

#### **movie-theater-frontend/src/contexts/AuthContext.js**
Global authentication state management using React Context:

- **User State**: Maintains current user data, authentication status, and loading states
- **Authentication Methods**: Login, logout, and registration functions with API integration
- **Session Persistence**: Handles authentication token storage and validation
- **Auto-refresh Logic**: Automatically refreshes user data and handles session expiration
- **Permission Checking**: Provides utilities for checking user permissions and email verification status
- **Context Provider**: Wraps application components to provide authentication state throughout component tree

This context enables consistent authentication behavior across all application components.

#### **movie-theater-frontend/src/contexts/NotificationContext.js**
Real-time notification management system:

- **Notification State**: Manages array of user notifications with read/unread status
- **Real-time Updates**: Polling mechanism for fetching new notifications from backend
- **CRUD Operations**: Functions for marking notifications as read, adding local notifications, and clearing notifications
- **Integration Points**: Connects with various components to trigger notifications for user actions
- **Performance Optimization**: Efficient state updates to prevent unnecessary re-renders

#### **movie-theater-frontend/src/api/movies.js**
Centralized API communication layer for movie-related operations:

- **HTTP Client Setup**: Axios configuration with base URLs and authentication headers
- **CRUD Functions**: Complete set of functions for movie operations (fetch, search, create, update, delete)
- **Error Handling**: Consistent error processing and user-friendly error messages
- **Request Optimization**: Proper use of HTTP methods and request/response transformation
- **Authentication Integration**: Automatic inclusion of auth tokens in API requests

Similar API modules exist for showtimes, bookings, users, and notifications, providing a clean separation between UI components and backend communication.

#### **movie-theater-frontend/src/styles/MovieList.css**
Comprehensive styling for movie browsing interface:

- **Responsive Grid Layout**: CSS Grid and Flexbox for movie card arrangements that work across device sizes
- **Filter Interface Styling**: Form controls, buttons, and layout for the filtering sidebar
- **Card Design**: Movie poster sizing, text layout, and hover effects
- **Mobile Optimization**: Media queries and responsive design for mobile devices
- **Loading States**: Styling for loading spinners and skeleton components
- **Accessibility**: Focus styles and color contrast for accessibility compliance

The CSS demonstrates modern responsive design principles with mobile-first approach and accessibility considerations.

### **Configuration Files**

#### **docker-compose.yml**
Multi-service container orchestration for local development:

- **Service Definitions**: Separate containers for backend, frontend, PostgreSQL database, and Redis
- **Network Configuration**: Inter-service communication setup
- **Volume Management**: Persistent data storage for database and file uploads
- **Environment Variables**: Service-specific configuration and secrets management
- **Development Optimization**: Hot reload configuration for both frontend and backend development

#### **backend/requirements.txt**
Python dependency specification for backend services:

Lists all required packages including Django, Django REST Framework, Celery, Redis client, PostgreSQL adapter, testing libraries, and deployment dependencies. Includes specific version numbers for reproducible builds.

#### **movie-theater-frontend/package.json**
Node.js project configuration and dependency management:

- **Dependencies**: React, React Router, Axios, testing libraries, and UI components
- **Scripts**: Development server, build process, testing, and deployment scripts
- **Build Configuration**: Webpack and Babel configuration for modern JavaScript features
- **Testing Setup**: Jest and React Testing Library configuration for comprehensive testing

---

## 🚀 How to Run the Application

### Prerequisites
- Docker and Docker Compose installed
- Node.js 14+ and Python 3.8+ for manual setup
- Git for cloning the repository

### Quick Start with Docker
```bash
git clone https://github.com/dalalEg/CS50W.git
cd movie_theater_project
docker compose up --build
```
