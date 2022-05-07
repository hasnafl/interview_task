from celery.schedules import crontab


# CELERY_IMPORTS = ["task.sending_email_with_celery"]
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'Asia/Singapore'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'task.sending_email_with_celery',
        # Every minute
        'schedule': crontab(minute="*")
    }
}