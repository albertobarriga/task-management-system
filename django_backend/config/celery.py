import os
from celery import Celery

# Establecer las settings de Django por defecto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Cargar configuración desde settings.py con prefijo CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodescubrir tareas en todas las apps instaladas (tasks.py)
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Tarea de debug para comprobar que Celery está funcionando.
    Ejecutar con: celery -A config call config.celery.debug_task
    """
    print(f"Request: {self.request!r}")
