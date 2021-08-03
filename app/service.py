from django.core.mail import send_mail
from ics import Calendar, Event
import requests
import arrow
from app.data import country

def send(user_email):
    """отправка сообщения на почту"""
    send_mail(
        'имя сообщения',  # менять !!!
        'дата и время',  # менять !!!
        'отвечать не нужно',
        [user_email],
        fail_silently=False
    )




