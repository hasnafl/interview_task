# interview_task
Python3 app.py
Run Celery Worker ===> celery --app=app.celery worker --loglevel=debug
Run Celery Beat ===> celery -A app.celery beat --schedule=/tmp/celerybeat-schedule --loglevel=INFO -pidfile=/tmp/celerybeat.pid
