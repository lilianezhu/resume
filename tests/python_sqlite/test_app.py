import os
import sqlite3
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "web", "python_sqlite")))

from app import app, get_db


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM posts")
            db.execute("DELETE FROM users")
            db.commit()
        yield client


def test_register_and_login_flow(client):
    response = client.post(
        "/register",
        data={"username": "alice", "password": "secret"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    login_response = client.post(
        "/login",
        data={"username": "alice", "password": "secret"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200
    assert b"Hello, alice" in login_response.data


def test_logged_in_user_can_post(client):
    client.post("/register", data={"username": "bob", "password": "12345"})
    client.post("/login", data={"username": "bob", "password": "12345"})

    post_response = client.post(
        "/posts",
        data={"content": "Hello from Flask"},
        follow_redirects=True,
    )
    assert post_response.status_code == 200
    assert b"Hello from Flask" in post_response.data


def test_guest_cannot_post(client):
    response = client.post(
        "/posts",
        data={"content": "Should not work"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Login" in response.data
