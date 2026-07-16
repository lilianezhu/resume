# Architecture: Flask + SQLite MVP

## Overview
The application follows a simple Flask MVC-style structure with:
- Routes for authentication and posting
- A SQLite database for users and posts
- Templates for registration, login, and home views
- A small test suite using Flask's test client

## Components

### 1. Application Layer
- `app.py`: creates the Flask app, registers routes, and initializes the database

### 2. Data Layer
- `database.py`: handles SQLite connection and schema creation
- `models.py` or helper functions: manages insert/select operations for users and posts

### 3. Presentation Layer
- `templates/`: HTML files for register, login, and home pages

### 4. Tests
- `tests/`: regression tests for registration, login, and post creation

## Data Model
### users
- `id` INTEGER PRIMARY KEY
- `username` TEXT UNIQUE NOT NULL
- `password_hash` TEXT NOT NULL

### posts
- `id` INTEGER PRIMARY KEY
- `user_id` INTEGER NOT NULL
- `content` TEXT NOT NULL
- `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP

## Request Flow
1. User visits `/register` or `/login`
2. Form data is posted to the server
3. Flask validates input and interacts with SQLite
4. Session data marks user as authenticated
5. Authenticated users can create posts from `/`
6. Posts are stored and displayed on the home page

## Security Notes
- Passwords are hashed with `werkzeug.security.generate_password_hash`
- Sessions use Flask's built-in session handling
- Only logged-in users can create posts
