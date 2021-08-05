from app.models import HisEvent
import calendar
from celery import shared_task
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from app.service import holidays


@shared_task
def remind_about_event(his_event_id):
    """Sends an event reminder by mail """
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
def holiday():
    """Run once a quarter """
    holidays()
