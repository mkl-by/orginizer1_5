import datetime
import re

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

        reg = re.compile(r"^(\d{4}(-?\d\d){2})[tT]?((\d\d:?){1,2}(\d\d)?(.\d{3})?([zZ]|[+-](\d\d):?(\d\d)))?$")
        string = f'{kwargs["year"]}-{kwargs["month"]}-{kwargs["day"]}'
        ymd = reg.search(string)
        if not ymd:
            return Response({
                    "message": f"Params date url .../year/month/day value error."
            },
                    status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ymd = datetime.datetime.strptime(string, '%Y-%m-%d')
        except ValueError:
            return Response({
                     "message": f"Date parameters in url .../year/month/day value error."
            },
                    status=status.HTTP_400_BAD_REQUEST
            )
        print(ymd)
        query_set = HisEvent.objects.filter(
            user=self.request.user,
            notified=False,
            remind_message__year=ymd.year,
            remind_message__month=ymd.month,
            remind_message__day=ymd.day).order_by('remind_message')

        serializer = HisEventSerializer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


