from app.models import HisEvent
import calendar
from celery import shared_task
from django.core.mail import send_mail


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
    except Exception as exc:
        raise remind_about_event.retry(exc=exc, max_retries=3)
