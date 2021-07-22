from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .data import choiscountry, tiktak
# Create your models here.


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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user')
    name_event = models.CharField(max_length=250)
    remind = models.CharField(max_length=20, choices=tiktak)  # оповещение
    data_start = models.DateTimeField()
    data_end = models.DateTimeField()

    def __str__(self):
        return f"user {self.user.id} --> дело: {self.name_event} --> оповещать {tiktak[self.remind][1]}"

