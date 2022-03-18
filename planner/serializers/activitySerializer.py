# Python
# Django
# Rest Framework
from rest_framework.serializers import ModelSerializer
# Local
from ..models import Activity
from .reservationSerializer import ActivityReservationSerializer
class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class FullActivitySerializer(ModelSerializer):

    reservations = ActivityReservationSerializer(source='reservation_set', many=True, read_only=True)
    class Meta:
        model = Activity
        fields = '__all__'