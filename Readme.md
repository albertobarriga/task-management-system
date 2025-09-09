Task Management System
A task management system built with Django, Celery, Redis and PostgreSQL, containerized with Docker.

TO START PROJECT:

## Quick Start
```bash
git clone https://github.com/albertobarriga/task-management-system.git
cd task-management-system
cp .env.sample .env
docker-compose up

🚀 Features
Django 4.2 - Main web framework

Celery - Asynchronous task processing

Redis - Message broker and cache

PostgreSQL - Database

Docker - Full application containerization

Gunicorn - WSGI server for production

📦 Included Services
web - Django application (port 8000)

db - PostgreSQL database (port 5432)

redis - Redis server (port 6379)

celery_worker - Celery worker

celery_beat - Celery task scheduler

🛠️ Installation
Prerequisites
Docker

Docker Compose

Configuration
Clone the repository

Create a .env file with environment variables:

env
DEBUG=1
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*

POSTGRES_DB=task_db
POSTGRES_USER=task_user
POSTGRES_PASSWORD=task_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

<!-- DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com -->
Execution
bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
📊 Project Structure
text
django_backend/
├── config/                 # Django configuration
├── management/            # Custom commands
├── scripts/              # Entrypoint scripts
├── requirements.txt      # Python dependencies
└── Dockerfile           # Docker configuration
🌐 Access
Application: http://localhost:8000

Django Admin: http://localhost:8000/admin (create superuser first)

🎯 Useful Commands
bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# View real-time logs
docker-compose logs -f

# Run migrations manually
docker-compose exec web python manage.py migrate

# Access database
docker-compose exec db psql -U task_user -d task_db

# Restart specific service
docker-compose restart web
🔧 Development
For development, you can mount volumes to sync code:

yaml
# In docker-compose.yml
volumes:
  - ./django_backend:/app
📝 Notes
Static files are served from /static/

Migrations are applied automatically on startup

Celery is configured for asynchronous task processing

Redis handles message queue and results

🚨 Troubleshooting
If you encounter errors:

Verify all variables in .env are correct

Run docker-compose down -v and rebuild

Check logs with docker-compose logs

