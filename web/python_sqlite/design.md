# Design: Flask + SQLite MVP

## Goals
Create a minimal but polished MVP that demonstrates:
- registration
- authentication
- authenticated posting
- basic persistence with SQLite

## User Stories
- As a new user, I want to register with a username and password.
- As a returning user, I want to log in securely.
- As a logged-in user, I want to post content.
- As a guest, I want to see the app but not post.

## Pages
### Landing Page `/`
- Shows a welcome message
- Displays posts from all users
- Gives logged-in users a form to create a new post
- Gives guests links to register and login

### Register Page `/register`
- Form with username and password fields
- Validates uniqueness of username
- Redirects to login on success

### Login Page `/login`
- Form with username and password
- Sets session on success
- Redirects to home on success

### Logout `/logout`
- Clears the session and redirects home

## UX Notes
- Use simple Bootstrap-like HTML styling for readability
- Show friendly error messages for invalid login or duplicate registration
- Keep the interface minimal so the MVP is easy to review

## Implementation Notes
- Use Flask `session` for authentication state
- Use SQLite `sqlite3` module directly or via Flask helpers
- Keep the app single-file for the MVP to reduce complexity
