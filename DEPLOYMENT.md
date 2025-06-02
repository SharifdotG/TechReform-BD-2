# Production Deployment Checklist

## Before Deploying to Production

### 1. Environment Variables

- [ ] Create a `.env` file based on `.env.example`
- [ ] Generate a new SECRET_KEY for production
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS with your domain names

### 2. Database Configuration

- [ ] Configure production database (PostgreSQL/MySQL recommended)
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

### 3. Static Files

- [ ] Configure static file serving (e.g., Nginx, WhiteNoise)
- [ ] Run: `python manage.py collectstatic`

### 4. Security

- [ ] Configure HTTPS
- [ ] Set up proper backup procedures
- [ ] Review and configure Django security settings

### 5. Media Files

- [ ] Configure media file storage (local or cloud)
- [ ] Set appropriate permissions for media directory

### 6. Dependencies

- [ ] Install production dependencies: `pip install -r requirements.txt`
- [ ] Consider using Docker for containerized deployment

## Quick Start for Development

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Start development server: `python manage.py runserver`

## Important Notes

- This project includes sample data and media files for demonstration
- Database file (`db.sqlite3`) should not be used in production
- Review all TODO/FIXME comments before production deployment
- Test all functionality thoroughly before deployment
