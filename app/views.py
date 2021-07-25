from app.models import HisEvent
from app.serializers import HisEventSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView


class HisEventListApiView(ListCreateAPIView):
    queryset = HisEvent.objects.all()
    serializer_class = HisEventSerializer
