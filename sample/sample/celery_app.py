import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sample.settings')

def create_celery_app():
    app = Celery('sample')
    
    # Using a string here means the worker doesn't have to serialize
    # the configuration object to child processes.
    app.config_from_object('django.conf:settings', namespace='CELERY')
    
    # Load task modules from all registered Django apps.
    app.autodiscover_tasks()
    
    # Explicitly import task modules to ensure they're discovered
    app.autodiscover_tasks(['todo'])
    
    # Print discovered tasks for debugging
    print("Celery app created successfully")
    print(f"Registered tasks: {list(app.tasks.keys())}")
    
    return app

# Create the celery app instance
celery_app = create_celery_app()

@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 