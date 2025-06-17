# PostgreSQL Local Setup Instructions

## Installation

### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### On macOS:
```bash
brew install postgresql
brew services start postgresql
```

### On Windows:
Download and install from: https://www.postgresql.org/download/windows/

## Database Setup

1. **Switch to postgres user and create database:**
```bash
sudo -u postgres psql
```

2. **In PostgreSQL shell:**
```sql
CREATE DATABASE techreform;
CREATE USER techreform WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE techreform TO techreform;
\q
```

3. **Update your local environment:**
Create a `.env` file in your project root:
```
DATABASE_URL=postgresql://techreform:your_password_here@localhost:5432/techreform
```

4. **Install python-dotenv** (if not already installed):
```bash
pip install python-dotenv
```

5. **Update settings.py** to load .env file:
Add this at the top of settings.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Alternative: Keep SQLite for Development

If you prefer to keep SQLite for local development, change the default back to:
```python
default='sqlite:///' + str(BASE_DIR / 'db.sqlite3')
```

This will work fine because Render will override with PostgreSQL via DATABASE_URL.
