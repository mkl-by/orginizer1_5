from django.utils import timezone
from rest_framework import serializers
from app.models import HisEvent

"""
ПАМЯТКА джуна:
Добавление кастомного поля в сериализер
MySerializer(serializers.HyperlinkedModelSerializer):
user = serializers.ReadOnlyField()
class Meta:
    model = My
    fields = ('user','title','description')

Когда вы вызываете сериализатор, вы просто добавляете текущего пользователя в сериализатор, 
либо в views.py или в методе создания сериализатора.

1. В views.py

serializer.save(user=request.user)

2. В сериализаторе создайте метод create

def create(self, validated_data):
    validated_data['user'] = request.user.id
    obj = ExampleModel.objects.create(**validated_data)
    return obj

"""


class HisEventSerializer(serializers.ModelSerializer):
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
                raise serializers.ValidationError("Yesterday has already passed ")
        except KeyError:
            # if data['data_end'] KeyError
            return data
        return data