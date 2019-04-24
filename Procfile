release: python manage.py migrate
web: gunicorn --bind=evening-inlet-45238.herokuapp.com:10000 TaskManager.wsgi
worker: python worker.py