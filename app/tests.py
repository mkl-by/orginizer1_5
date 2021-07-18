from json import dumps

from django.test import TestCase
from django.core import mail

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import MyUser
from .data import choiscountry
from django.conf import settings
from django.contrib.auth import get_user_model
from app.utils import pars_mail


class AccountTests(APITestCase):
    # APITestCase use APIClient instead of Django's default Client
    settings.EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    settings.EMAIL_FILE_PATH = settings.BASE_DIR / 'mail_log_file'

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
        response = self.client.post('/auth/users/', data=dumps(data), content_type="application/json")
        # check status msg 201
        print(response.data)

        t = pars_mail(settings.EMAIL_FILE_PATH)
        uid = t[0]
        token = t[1]
        print(uid, token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(response.data['email'], 'test@test.test')
        self.assertEqual(response.data['country'], choiscountry()[0][0])
        # check creating user obj
        user = MyUser.objects.get(id=response.data['id'])
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['country'], user.country)
    #     # check creating token obj
    #     self.assertEqual(
    #         Token.objects.get(user=user).__str__(),
    #         response.json()['token']
    #     )
    #     self.assertEqual(len(mail.outbox), 1)

        # print(settings.DJOSER['ACTIVATION_URL'])
    #     # BAD CASE
    #     data['email'] = 'bad_emaild'
    # #     print(data)
    #     response = self.client.post('auth/users/', data=dumps(data), content_type="application/json")
    # #     # check status 400
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
    # #     # check user obj isn't created
    #     self.assertEqual(MyUser.objects.filter(email=data['email']).exists(), False)

    # # def test_get_token(self):
    #     """
    #     Ensure we can get or create token
    #     """
    #     url = reverse('get-token')
    #     User_model = get_user_model()   # CustomUser model
    #     user = User_model.objects.create_user(
    #         email='test@test.test',
    #         password='password',
    #         country=None
    #     )
    #     token = Token.objects.create(user=user)
    #     # GOOD CASE
    #     data = {
    #         'email': 'test@test.test',
    #         'password': 'password'
    #     }
    #     response = self.client.post(url, data=dumps(data), content_type="application/json")
    #     # check get token
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
    #     self.assertEqual(response.json()['token'], token.__str__())
    #     # check create token
    #     token.delete()
    #     response = self.client.post(url, data=dumps(data), content_type="application/json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
    #     self.assertEqual(
    #         Token.objects.get(user=user).__str__(),
    #         response.json()['token']
    #     )
    #     # BAD CASE
    #     data['password'] = 'bad_password'
    #     response = self.client.post(url, data=dumps(data), content_type="application/json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
# class UserTestCase(APITestCase):
#     profile_list_url = reverse('all-profiles')
#     def setUp(self):
#         data = {
#             'email': 'test@test.test',
#             'password': 'password',
#             'country': choiscountry()[0][0],
#         }
#         # создайте нового пользователя, отправив запрос к конечной точке djoser
#         self.user=self.client.post('/auth/users/',data=data)
#         # получить веб-токен JSON для вновь созданного пользователя
#         response=self.client.post('/auth/jwt/create/',data={'username':'mario','password':'i-keep-jumping'})
#         self.token=response.data['access']
#         self.api_authentication()
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)
#
#     # получить список всех профилей пользователей во время аутентификации пользователя запроса
#     def test_userprofile_list_authenticated(self):
#         response=self.client.get(self.profile_list_url)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
#
#     # получить список всех профилей пользователей, пока запрос пользователя не прошел проверку подлинности
#     def test_userprofile_list_unauthenticated(self):
#         self.client.force_authenticate(user=None)
#         response=self.client.get(self.profile_list_url)
#         self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
#
#     # проверьте, чтобы получить данные профиля аутентифицированного пользователя
#     def test_userprofile_detail_retrieve(self):
#         response=self.client.get(reverse('profile',kwargs={'pk':1}))
#         # print(response.data)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
#
#
#     # заполнить профиль пользователя, который был автоматически создан с использованием сигналов
#     def test_userprofile_profile(self):
#         profile_data={'description':'I am a very famous game character','location':'nintendo world','is_creator':'true',}
#         response=self.client.put(reverse('profile',kwargs={'pk':1}),data=profile_data)
#         print(response.data)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)