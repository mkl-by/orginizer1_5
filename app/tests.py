import datetime
import time
from json import dumps

# from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail

# from django.urls import reverse
from django.utils import timezone
from pytz import tzinfo
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from app.models import MyUser, HisEvent
from app.data import choiscountry, tiktak
from django.conf import settings
# from django.contrib.auth import get_user_model
from app.utils import pars_mail


class AccountTests(APITestCase):
    # APITestCase use APIClient instead of Django's default Client
    # settings.EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    # settings.EMAIL_FILE_PATH = settings.BASE_DIR / 'mail_log_file'

    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    def test_register(self):
        """
        Ensure we can create a new CustomUser object and Token object
        """
        # GOOD CASE
        data = {
            'email': 'test@test.test',
            'password': 'useruser',
            'country': choiscountry()[0][0],
        }
        # register user
        response = self.client.post('/auth/users/', data=dumps(data), content_type="application/json")
        # check status msg 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(response.data['email'], 'test@test.test')
        self.assertEqual(response.data['country'], choiscountry()[0][0])
        # check creating user obj
        user = MyUser.objects.get(id=response.data['id'])
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['country'], user.country)

        # confirmation of activation by email "активируем юзера по из почты"
        # проверили, что отправили одно сообщение
        self.assertEqual(len(mail.outbox), 1)

        uid, token = pars_mail(mail.outbox[0].body)
        data_token = {
            'uid': uid,
            'token': token,
        }

        response_activate = self.client.post(
            '/auth/users/activation/',
            data=dumps(data_token),
            content_type="application/json"
        )

        self.assertEqual(response_activate.status_code, status.HTTP_204_NO_CONTENT, msg=response_activate.data)
        self.assertEqual(response_activate.data, None)

        # login user and return token user "логинимся и получаем в ответ токен usera"
        data_user = {
            'email': 'test@test.test',
            'password': 'useruser',
        }

        response_login = self.client.post(
            '/auth/token/login/',
            data=dumps(data_user),
            content_type="application/json"
        )

        self.assertEqual(response_login.status_code, status.HTTP_200_OK, msg=response_login.data)

        # check token obj
        self.assertEqual(
            Token.objects.get(user=user).__str__(),
            response_login.data['auth_token']
        )

        # BAD CASE
        data['email'] = 'bad_emaild'
        response = self.client.post('auth/users/', data=dumps(data), content_type="application/json")
        # check status 400
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # check user obj isn't created
        self.assertEqual(MyUser.objects.filter(email=data['email']).exists(), False)

    def test_get_token(self):
        """ Ensure we can get or create token """
        user_model = get_user_model()   # CustomUser model
        user = user_model.objects.create_user(
            email='test@test.test',
            password='password',
            country=choiscountry()[0][0]
        )
        token = Token.objects.create(user=user)
        # GOOD CASE
        data = {
            'email': 'test@test.test',
            'password': 'password',
            # 'country': choiscountry()[0][0]
        }
        response = self.client.post('/auth/token/login/', data=dumps(data), content_type="application/json")
        # check get token
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data['auth_token'], token.__str__())
        # check create token
        token.delete()
        response = self.client.post('/auth/token/login/', data=dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(
            Token.objects.get(user=user).__str__(),
            response.data['auth_token']
        )

        # BAD CASE
        data['password'] = 'bad_password'
        response = self.client.post('/auth/token/login/', data=dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

    def test_create_his_event(self):
        """проверка модели сообщения"""
        user = MyUser.objects.create_user('mmm@mmm.mm', choiscountry()[0][0], 'password')
        self.assertEqual(user.email, 'mmm@mmm.mm')
        self.assertEqual(user.country, 'Afghanistan')
        self.assertNotEqual(user.password, 'password')

        mess = HisEvent.objects.create(
            user=user,
            name_event='name_event',
            data_start=datetime.datetime(2021, 7, 22, 16, 30, tzinfo=datetime.timezone.utc),
            data_end=datetime.datetime(2021, 7, 22, 17, 0, tzinfo=datetime.timezone.utc),
            remind=tiktak[1][0]
        )
        self.assertEqual(mess.id, user.id)
        self.assertEqual(mess.name_event, 'name_event')
        self.assertEqual(mess.remind, 1)



