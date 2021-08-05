from django.urls import path

from app.views import HisEventListApiView, HisEventDayListApiView

urlpatterns = [
    #  add remind
    path('', HisEventListApiView.as_view(), name='create_event'),
    path('listofday/<str:year>/<str:month>/<str:day>', HisEventDayListApiView.as_view(), name='list_of_day'),
    #path('holidays/<str:year>/<str:month>/', HolidayListApi.as_view(), name='holidayapi'),
    # path('loginuser/', views.LoginUser.as_view(), name='loginuser'),
    # path('logout/', views.logout_view, name='logout'),
    # path('rating/<int:hotel_id>/<str:name_hotel>/', views.Raiting.as_view(), name='rating'),
    # path('rating-ajax/', views.Raiting.as_view()),
    # path('api_hotels/', HotelsListApiView.as_view()),
    # path('api/room/<int:hotel_id>/', RoomsListApiView.as_view()),
    # path('api/<int:hotel_id>/', BookingListApiView.as_view()),
  ]