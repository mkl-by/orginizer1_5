from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import HisEvent, HolidaysModel, MyUser
from app.serializers import HisEventCreateSerializer, HisEventSerializer, HolidaysSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, GenericAPIView

from app.service import creation_date


class MixinView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class HisEventListApiView(ListCreateAPIView, MixinView):

    serializer_class = HisEventCreateSerializer

    def get_queryset(self):
        """return hisevent of user"""
        return HisEvent.objects.filter(user=self.request.user)


class HisEventDayListApiView(ListAPIView, MixinView):
    """" Returns user events in the selected date (one day)"""
    serializer_class = HisEventSerializer

    def get(self, request, *args, **kwargs):

        # reg = re.compile(r"^(\d{4}(-?\d\d){2})[tT]?((\d\d:?){1,2}(\d\d)?(.\d{3})?([zZ]|[+-](\d\d):?(\d\d)))?$")
        string = f'{kwargs["year"]}-{kwargs["month"]}-{kwargs["day"]}'
        # ymd = reg.search(string)
        # if not ymd:
        #     return Response({
        #             "message": f"Params date url .../year/month/day value error."
        #     },
        #             status=status.HTTP_400_BAD_REQUEST
        #     )
        ymd = creation_date(string)

        query_set = HisEvent.objects.filter(
                                user=self.request.user,
                                notified=False,
                                remind_message__year=ymd.year,
                                remind_message__month=ymd.month,
                                remind_message__day=ymd.day).order_by('remind_message')

        if not query_set:
            return Response({
                "message": f"{ymd.day}.{ymd.month}.{ymd.year} no events"
            },
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            )

        serializer = HisEventSerializer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HolidayListApi(ListAPIView, MixinView):
    """Returns holidays for the month"""

    serializer_class = HolidaysSerializer

    def get(self, request, *args, **kwargs):
        country = MyUser.objects.get(email=self.request.user).country
        if not country:
            return Response({
                "message": f"We do not know where you come from, you did not indicate the country at registration."
            },
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        string = f'{kwargs["year"]}-{kwargs["month"]}-01'
        ymd = creation_date(string)

        query_set = HolidaysModel.objects.filter(
                                country=country,
                                datestartholiday__year=ymd.year,
                                datestartholiday__month=ymd.month,
                                ).order_by('holidays')

        if not query_set:
            return Response({
                "message": "In the database there is no data on holidays on your request "
            },
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            )

        serializer = HolidaysSerializer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)








