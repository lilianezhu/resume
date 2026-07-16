# Proposal: Flask + SQLite Authentication and Posting App

## Goal
Build a small web application that lets users register and log in with a username and password stored in SQLite. Only authenticated users can create posts. The app will provide a simple MVP with clear routes, a minimal database schema, and basic tests.

## Scope
- User registration with a unique username
- User login with password verification
- Session-based authentication
- Authenticated users can create posts
- Anonymous users can view the landing page and login/register forms
- SQLite database for persistence
- Flask app structure suitable for future expansion

## Success Criteria
- Users can register and log in
- Only logged-in users can submit a post
- Posts are stored in SQLite and shown on the main page
- App includes a simple test suite to prevent regressions

## Stack
- Python
- Flask
- SQLite3
- pytest
- Flask test client
