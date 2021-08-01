import datetime

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import HisEvent
from app.serializers import HisEventCreateSerializer, HisEventSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView


class HisEventListApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = HisEventCreateSerializer

    def get_queryset(self):
        """return hisevent of user"""
        return HisEvent.objects.filter(user=self.request.user)


class HisEventDayListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = HisEventSerializer
    #serializer_class = HisEventCreateSerializer


    def get(self, request, *args, **kwargs):

        dictofday = {
            'year': 0,
            'month': 0,
            'day': 0,
              }

        for key in dictofday:
            dmy = self.request.query_params.get(key)
            print(dmy)
            # if type(int(dmy)) != int:
            #     return Response({
            #         "message": f"User with params `{key}` value error."},
            #         status=status.HTTP_400_BAD_REQUEST)
            # осуществить проверку года, дня и месяца!!!!!!!!!!!!!!
            dictofday[key] = int(dmy)

            d = datetime.datetime(dictofday['year'], dictofday['month'], dictofday['day'])
        query_set = HisEvent.objects.filter(
            user=self.request.user,
            notified=False,
            remind_message__year=d.year).order_by('remind_message')
        # query_set = HisEvent.objects.filter(
        #             user=self.request.user,
        #             notified=False,
        #             remind_message__day=dictofday['day'],
        #             remind_message__month=dictofday['month'],
        #             remind_message__year=dictofday['year']).order_by('remind_message')
        serializer = HisEventSerializer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


