import datetime
import json
from json import dumps

import arrow
import requests
from django.contrib.auth import get_user_model
from django.core import mail

from django.urls import reverse
from django.utils import timezone
from ics import Calendar

from rest_framework import status
from rest_framework.test import APITestCase, APIClient, RequestsClient
from rest_framework.authtoken.models import Token
from app.models import MyUser, HisEvent, HolidaysModel
from app.data import choiscountry, tiktak
from django.conf import settings
from app.utils import pars_mail


class AccountTests(APITestCase):
    # APITestCase use APIClient instead of Django's default Client
    # settings.EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    # settings.EMAIL_FILE_PATH = settings.BASE_DIR / 'mail_log_file'

    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    datas = {
        'data_start': timezone.now()+datetime.timedelta(hours=1, seconds=15),
        'data_end': timezone.now()+datetime.timedelta(hours=3),
        'name_event': 'name_event',
        'remind': tiktak[0][0],
    }
    user_data = {
        'email': 'test@test.test',
        'password': 'useruser',
        'country': choiscountry()[0][0],
    }

    def test_register(self):
        """
        Ensure we can create a new CustomUser object and Token object
        """
        # GOOD CASE
        # register user
        response = self.client.post('/auth/users/', data=dumps(self.user_data), content_type="application/json")

        # check status msg 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(response.data['email'], 'test@test.test')
        self.assertEqual(response.data['country'], choiscountry()[0][0])
        # check creating user obj
        user = MyUser.objects.get(id=response.data['id'])
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['country'], user.country)

        # confirmation of activation by email "активируем юзера из почты"
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

        data_user = self.user_data.copy()
        data_user.pop('country')

        response_login = self.client.post('/auth/token/login/', data=dumps(data_user),
                                                                content_type="application/json")

        self.assertEqual(response_login.status_code, status.HTTP_200_OK, msg=response_login.data)

        # check token obj
        self.assertEqual(
            Token.objects.get(user=user).__str__(),
            response_login.data['auth_token']
        )

        # BAD CASE
        self.user_data['email'] = 'bad_emaild'
        response = self.client.post('auth/users/', data=dumps(self.user_data), content_type="application/json")
        # check status 400
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # check user obj isn't created
        self.assertEqual(MyUser.objects.filter(email=self.user_data['email']).exists(), False)

    def test_get_token(self):
        """ Ensure we can get or create token """
        user_model = get_user_model()   # CustomUser model
        user = user_model.objects.create_user(**self.user_data)
        token = Token.objects.create(user=user)
        # GOOD CASE
        data = self.user_data.copy()
        data.pop('country')
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
        """HisEvent models"""
        user = MyUser.objects.create_user('mmm@mmm.mm', choiscountry()[0][0], 'password')
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, 'mmm@mmm.mm')
        self.assertEqual(user.country, 'Afghanistan')
        self.assertNotEqual(user.password, 'password')

        data = {
            'user': user,
            'data_start': timezone.now()+datetime.timedelta(hours=1, seconds=15),
            'data_end': timezone.now()+datetime.timedelta(hours=3),
            'name_event': 'name_event',
            'remind': tiktak[0][0],
        }

        for i in range(2):
            if i == 0:
                event = HisEvent.objects.create(**data)
                self.assertEqual(event.data_end, data['data_end'])
                self.assertEqual(event.id, 1)
                self.assertEqual(event.remind_message, data['data_start']-datetime.timedelta(hours=data['remind']))
                self.assertEqual(event.remind, 1)
                self.assertFalse(event.notified)
            else:
                # It is worked out an hour later
                data.pop('data_end')
                data['remind'] = None
                event = HisEvent.objects.create(**data)
                self.assertEqual(event.id, 2)
                # user not add data_end
                self.assertEqual(event.data_end, (datetime.timedelta(days=1) + data['data_start']).
                                 replace(hour=0, minute=0, second=0))
                # user not add remind

                self.assertIsNone(event.remind)
                self.assertFalse(event.notified)

            self.assertEqual(event.name_event, 'name_event')
            self.assertEqual(event.data_start, data['data_start'])
            self.assertFalse(event.notified)

    def test_create_country(self):
        """HolidaysModel model"""
        countryy = ['Afghanistan', 'Gibraltar', 'Saint Vincent and the Grenadines']
        for con in countryy:
            url = f"https://www.officeholidays.com/ics/ics_country.php?tbl_country={con}"
            c = Calendar(requests.get(url).text)
            data = list(c.timeline)
            for i in data:
                HolidaysModel.objects.update_or_create(
                    country=con,
                    holidays=i.name,
                    datestartholiday=str(i.begin),
                    dateendholiday=str(i.end)
                    )
                model = HolidaysModel.objects.last()
                self.assertEqual(model.country, con)
                self.assertTrue(model.holidays, i.name)
                self.assertEqual(arrow.Arrow.fromdatetime(model.datestartholiday), i.begin)
                self.assertEqual(arrow.Arrow.fromdatetime(model.dateendholiday), i.end)

    def test_remind_messages(self):
        """test all events for the month"""
        user_model = get_user_model()   # CustomUser model
        user = user_model.objects.create_user(**self.user_data)
        dat = self.datas.copy()
        dat['user'] = user

        data = self.user_data.copy()
        data.pop('country')

        HisEvent.objects.create(**dat)

        self.client.post('/auth/token/login/', data=dumps(data), content_type="application/json")
        token = Token.objects.first()
        clients = RequestsClient()
        response1 = clients.get('http://testserver/eventmonth/2021/08/',
                                headers={'Authorization': 'Token ' + token.key})

        query = HisEvent.objects.filter(
            remind_message__month=timezone.now().month,
            user=user)

        dict_event = {}
        for dd in query.dates('remind_message', 'day'):
            list_event_day = list(query.filter(remind_message__day=dd.day).values_list('name_event', flat=True))
            dict_event[str(dd.day)] = list_event_day

        self.assertEqual(eval(json.loads(response1.text)), dict_event)
