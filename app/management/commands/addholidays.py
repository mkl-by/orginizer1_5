from django.core.management.base import BaseCommand

from app.service import holidays


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """ When you first start the application,
        run the 'python manage.py addcountry' command.
        Fills the table with the holidays when the application is first started."""
        holidays()
