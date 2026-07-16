# Flask + SQLite MVP

This folder contains a simple Flask application with:
- user registration
- user login
- session-based authentication
- authenticated post creation
- SQLite persistence

## Requirements
- Python 3.11+
- Flask

## Setup
From the project root:

```powershell
cd C:\Users\arsli\OneDrive\Documents\resume
.venv311\Scripts\Activate.ps1
pip install flask
python web/python_sqlite/app.py
```

Then open:

```text
http://127.0.0.1:5000/
```
<img width="722" height="376" alt="image" src="https://github.com/user-attachments/assets/0f380397-d1db-4c44-b166-1c3163d370ee" />


## Run tests

```powershell
pytest -q tests/python_sqlite
```
