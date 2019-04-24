release: python manage.py migrate
web: gunicorn --bind=52.21.245.216:10000 TaskManager.wsgi
worker: python worker.py