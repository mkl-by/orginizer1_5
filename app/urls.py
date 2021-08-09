from django.urls import path

from app.views import HisEventListApiView, HisEventDayListApiView, HolidayListApi, EventMonthListApi

urlpatterns = [
    #  add remind
    path('', HisEventListApiView.as_view(), name='create_event'),
    path('listofday/<str:year>/<str:month>/<str:day>', HisEventDayListApiView.as_view(), name='list_of_day'),
    path('holidays/<str:year>/<str:month>/', HolidayListApi.as_view(), name='holidayapi'),
    path('eventmonth/<str:year>/<str:month>/', EventMonthListApi.as_view(), name='loginuser'),
  ]