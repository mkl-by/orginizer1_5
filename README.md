# Orginizer


Back-end (REST API) for application with authorization, the ability to add custom events and notifications about upcoming events and holidays in user's country by e-mail. Periodic update of the list of holidays.


Supported authentication backends

    Token based authentication from DRF

Supported Python versions

    Python 3.5
    Python 3.6
    Python 3.7
    Python 3.8

Supported Django versions

    Django 1.11
    Django 2.2
    Django 3.1

Supported Django Rest Framework versions

    Django Rest Framework 3.9
    Django Rest Framework 3.10
    Django Rest Framework 3.11


Available endpoints

    /users/
    /users/me/
    /users/confirm/
    /users/resend_activation/
    /users/set_password/
    /users/reset_password/
    /users/reset_password_confirm/
    /users/set_username/
    /users/reset_username/
    /users/reset_username_confirm/
    /token/login/ (Token Based Authentication)
    /token/logout/ (Token Based Authentication)

Before the first server start, execute the command
    
    python3 manage.py addholidays
next

    docker run -d -p 6379:6379 redis
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
    celery -A orginizer1_5 worker -l info
    celery -A orginizer1_5 beat -l info
    celery -A orginizer1_5 flower --port=5555

User authentication 
    
        post: ../auth/users/
        enter key form-data:
            email: your email 
            password: your password
            country: your country (choices)
                        
            Response => `{
                        "country": "Belarus",
                        "email": "mkl-byy@yandex.ru",
                        "id": 4
                    }`
User activation

       Emeil will be sent to the post:
       example: 'http:..../activate/NA/ar64ng-94463acc5ff501c24afa71de61511ef4'
         
            post: ../auth/users/activation/
            enter key form-data:
            uid: NA
            token: ar64ng-94463acc5ff501c24afa71de61511ef4
         response => 1

User login
        
        post: ../auth/token/login/
            enter key form-data:
            email: your email
            password: you password
            
         response => `{
                        "auth_token": "0fcd65a9db95d4f96d5275f7e20fc3578261bbb7"
                      }`

User logout

        post: ../auth/token/logout
             enter key headers:
            'Authorization': 'Token 0fcd65a9db95d4f96d5275f7e20fc3578261bbb7'
             response => 1

###### Create user event
        
        post: ../
        enter key form-data:
            name_event: text event 
            remind: (choices)
            data_start: YYYY-mm-dd hh:mm
            data_end: YYYY-mm-dd hh:mm
            enter key headers:
                'Authorization': 'Token ...'
        response =>
        
        {
            "name_event": "проверка",
            "remind": 1,
            "data_start": "2021-08-11T16:55:00+03:00",
            "data_end": "2021-08-11T19:30:00+03:00" 
        }
        
        if data save in db, start task remind_about_event,
        send a letter to the mail. 
    
        get: ../ - return all events
             enter key headers:
                'Authorization': 'Token ...'

###### User list of events for the day
    get: ../listofday/<YYYY>/<mm>/<dd>
    example: http://127.0.0.1:8000/listofday/2021/08/04

###### User list of holidays for the month
    get: ../holidays/<YYYY>/<dd>/
    example: http://127.0.0.1:8000/holidays/2021/08/

###### User list of events for the month  
    get: ../eventmonth/<YYYY>/<dd>/
    example: http://127.0.0.1:8000/eventmonth/2021/08
    
    
 # Start from Doker File
 
 add to settings for postgres
    
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRES_DB"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"), 
        'USER': os.environ.get("POSTGRES_USER"), 
        'HOST': 'db', 
        'PORT': 5432
        }  
    }
   
   Disable debug 
   
   Place the project in the folder orginizer
   
    run docker-compose up --build
    
   
 
            
   
