release: python manage.py migrate
web: gunicorn --bind=0.0.0.0:10000 TaskManager.wsgi
worker: python worker.py