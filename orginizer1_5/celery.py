import os
from celery import Celery
from celery.schedules import crontab

# указываем где находится джанговский модуль settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orginizer1_5.settings')

app = Celery('orginizer1_5')
app.config_from_object('django.conf:settings', namespace='CELERY')  # в сетингах настройки для селери начинаются с
# namespace

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'tasks.holidays',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
    },
}

app.autodiscover_tasks()  # нужна для автоматического подключения файлов tasks.py

