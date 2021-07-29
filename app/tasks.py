# from django.utils import timezone
from orginizer1_5.celery import app as appp
from app.models import HisEvent
import app.models # else: (most likely due to a circular import)
import calendar
# import datetime
from celery import shared_task
from django.core.mail import send_mail


# from django.db.models import Q
# from orginizer1_5.settings import DEFAULT_FROM_EMAIL

#
#
# @shared_task
# def remind_about_event():
#     events = models.HisEvent.objects.filter(notified=False, remind_message__gte=timezone.now()).select_related('user')
#     for event in events:
#         print(event.name_event)

# @app.task(bind=True)
# def send_twitter_status(self, oauth, tweet):
#     try:
#         twitter = Twitter(oauth)
#         twitter.update_status(tweet)
#     except (Twitter.FailWhaleError, Twitter.LoginError, Exception) as exc:
#         raise self.retry(exc=exc, max_retries=5)  # повторяем если не произошла ошибка
# написать проверки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@shared_task
def remind_about_event(his_event_id):
    event = HisEvent.objects.select_related('user').get(id=his_event_id)
    mon = calendar.month_name[event.data_start.month]  # mon БУКАВКАМИ
    send_mail(
        'Event reminder',
        f'ATTENTION \n{event.name_event} \n\
        {event.data_start.day} {mon} c {event.data_start.strftime("%H:%M")} по {event.data_end.strftime("%H:%M")}',
        f'{event.user.email}',
        [event.user.email],
        fail_silently=False,
    )
