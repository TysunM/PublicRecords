# app/worker.py
from .main import app  # Your FastAPI app
from celery import Celery
import os

# Configure Celery
celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery_app.conf.update(
    task_track_started=True,
)

# Optional: Add a simple test task
@celery_app.task
def add(x, y):
    return x + y
