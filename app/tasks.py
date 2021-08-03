from django.contrib.sites import requests
from ics import Calendar

from app.models import HisEvent, HolidaysModel
import calendar
from celery import shared_task
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from app.data import country

@shared_task
def remind_about_event(his_event_id):
    try:
        event = HisEvent.objects.select_related('user').get(id=his_event_id)
        mon = calendar.month_name[event.data_start.month]  # mon БУКАВКАМИ
        send_mail(
            'Event reminder',
            f'ATTENTION\n{event.name_event}\n\
            {event.data_start.day} {mon} c {event.data_start.strftime("%H:%M")} по {event.data_end.strftime("%H:%M")}',
            f'{event.user.email}',
            [event.user.email],
            fail_silently=False,
        )
        event.notified = True
    except ObjectDoesNotExist:  # if test works
        return 'Run test'
    except Exception as exc:
        raise remind_about_event.retry(exc=exc, max_retries=3)

@shared_task
def holidays():
    for con in country:
        url = f"https://www.officeholidays.com/ics/ics_country.php?tbl_country={con}"
        c = Calendar(requests.get(url).text)
        data = list(c.timeline)
        for i in data:
            HolidaysModel.objects.update_or_create(
                    country=con,
                    holidays=i.name,
                    datestartholiday=i.begin,
                    dateendholiday=i.end
                )
