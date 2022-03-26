# Python
# Django
# Rest Framework
from datetime import datetime
from decimal import getcontext
from multiprocessing import context
from django.forms import ValidationError
from rest_framework.serializers import ModelSerializer
# Local
from ..models import Activity
from .reservationSerializer import ActivityReservationSerializer
from ..enums import Repeat
class ActivitySerializer(ModelSerializer):
    def validate(self, data):
        repeat = data.get('repeat')
        repeatUntil = data.get('repeatUntil')
        endTime = self.context.get('request').data.get('endTime')

        if repeat != Repeat.NEVER and repeatUntil is None:
            raise ValidationError("Repeat Until cannot be null if the Repeat value is not Never")

        if repeatUntil is not None:
            endTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S%z")
            if repeatUntil < endTime:
                raise ValidationError("Valid Until date should be a later date than the End Date")

        return super().validate(data)
    class Meta:
        model = Activity
        fields = '__all__'

class FullActivitySerializer(ModelSerializer):

    reservations = ActivityReservationSerializer(source='reservation_set', many=True, read_only=True, context=getcontext())
    class Meta:
        model = Activity
        fields = '__all__'