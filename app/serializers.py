import datetime

from django.utils import timezone
from rest_framework import serializers
from app.models import HisEvent, HolidaysModel


class HolidaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidaysModel
        fields = ['holidays', 'datestartholiday', 'dateendholiday']


class HisEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HisEvent
        fields = '__all__'


class HisEventCreateSerializer(serializers.ModelSerializer):
    # создаем невидимое поле в с юзером который зарегистрирован
    # при запросе данные юзера вводить не нужно
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = HisEvent
        fields = ['user', 'name_event', 'remind', 'data_start', 'data_end']

    def validate(self, data):
        """
        Check that start is before finish.
        """
        try:
            if data['data_start'] > data['data_end']:
                raise serializers.ValidationError("finish must occur after start")
            if data['data_start'] < timezone.now():
                raise serializers.ValidationError("Yesterday has already passed")
            if data['remind']:
                if data['data_start'] - datetime.timedelta(hours=data['remind']) < timezone.now():
                    raise serializers.ValidationError("Reminder before the date")
        except KeyError:
            # if data['data_end'] KeyError
            return data
        return data
