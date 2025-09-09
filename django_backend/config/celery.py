import os
from celery import Celery
from celery.schedules import crontab

# settings of Django default
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Load config from settings.py with prefix CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in apps instaled
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-overdue-tasks-hourly': {
        'task': 'apps.tasks.tasks.check_overdue_tasks',
        'schedule': crontab(minute=0, hour='*/1'),  # Every hour
    },
    'cleanup-archived-tasks-weekly': {
        'task': 'apps.tasks.tasks.cleanup_archived_tasks', 
        'schedule': crontab(day_of_week='sunday', hour=2, minute=0),  # Every Sunday at 2 AM
    },
}

app.conf.timezone = 'UTC'
