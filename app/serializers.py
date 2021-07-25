import datetime

from rest_framework import serializers
from app.models import HisEvent


class HisEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HisEvent
        fields = ['id', 'user', 'name_event', 'remind', 'data_start', 'data_end']

    def validate(self, data):
        """
        Check that start is before finish.
        """
        try:
            if data['data_start'] > data['data_end']:
                raise serializers.ValidationError("finish must occur after start")
        except KeyError:
            # if data['data_end'] KeyError
            return data
        return data