web: gunicorn core.wsgi
worker: celery -A core worker -l info -P solo