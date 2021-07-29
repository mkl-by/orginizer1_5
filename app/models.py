import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from .data import choiscountry, tiktak


class MyUserManager(BaseUserManager):
    def create_user(self, email, country, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            country=country,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, country, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            country=country,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """Определяем свою модель юзера"""

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    country = models.CharField(max_length=120, choices=choiscountry())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['country']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class HisEvent(models.Model):
    """model user event"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name_event = models.CharField(max_length=250)
    remind = models.SmallIntegerField(null=True, blank=True, choices=tiktak)  # оповещение
    data_start = models.DateTimeField()
    data_end = models.DateTimeField(blank=True)
    remind_message = models.DateTimeField(null=True, blank=True)
    notified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """if the user has not set the data_end"""
        if self.data_end is None:
            self.data_end = (datetime.timedelta(days=1) + self.data_start).replace(hour=0, minute=0, second=0)
        if self.remind:
            self.remind_message = self.data_start - datetime.timedelta(hours=self.remind)
        else:
            self.remind_message = self.data_start
        super().save()
        from app.tasks import remind_about_event   # Tried from looping
        remind_about_event.apply_async((self.id,), eta=self.remind_message, retry=True, retry_policy={
            'max_retries': 2,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.2,
        })

    def __str__(self):
        return self.name_event
