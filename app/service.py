from django.core.mail import send_mail


def send(user_email):
    """отправка сообщения на почту"""
    send_mail(
        'имя сообщения',  # менять !!!
        'дата и время',  # менять !!!
        'отвечать не нужно',
        [user_email],
        fail_silently=False
    )
