from django.utils import timezone

# from orginizer1_5.celery import app
# import datetime
# from celery import shared_task
# from django.core.mail import send_mail
# from django.db.models import Q
# from orginizer1_5.settings import DEFAULT_FROM_EMAIL
# from app.models import HisEvent
#
#
# @shared_task
# def remind_about_event():
#     events = HisEvent.objects.filter(notified=False, remind_message__lte=timezone.now()).select_related('user')
#     for event in events:
#         print(event.name_event)
