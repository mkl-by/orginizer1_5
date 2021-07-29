
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from app.models import HisEvent
from app.serializers import HisEventSerializer
from rest_framework.generics import ListCreateAPIView


class HisEventListApiView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = HisEventSerializer

    def get_queryset(self):
        """return hisevent of user"""
        return HisEvent.objects.filter(user=self.request.user)