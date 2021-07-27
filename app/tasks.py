# from django.utils import timezone

from orginizer1_5.celery import app
#import datetime
from celery import shared_task
# from django.core.mail import send_mail
# from django.db.models import Q
# from orginizer1_5.settings import DEFAULT_FROM_EMAIL
# from app.models import HisEvent
#
#
# @shared_task
# def remind_about_event():
#     events = HisEvent.objects.filter(notified=False, remind_message__gte=timezone.now()).select_related('user')
#     for event in events:
#         print(event.name_event)

# @app.task(bind=True)
# def send_twitter_status(self, oauth, tweet):
#     try:
#         twitter = Twitter(oauth)
#         twitter.update_status(tweet)
#     except (Twitter.FailWhaleError, Twitter.LoginError, Exception) as exc:
#         raise self.retry(exc=exc, max_retries=5)  # повторяем если не произошла ошибка

@shared_task
def print_task(x, y):
    print(f'выполнена таска {x} и {y}')

