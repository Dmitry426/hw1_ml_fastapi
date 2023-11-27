from celery import Celery

celery = Celery("worker")

celery.config_from_object("app.settings.celery_config")
