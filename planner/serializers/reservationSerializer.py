# Python
# Django
# Rest Framework
from rest_framework.serializers import ModelSerializer
# Local
from ..models import Reservation


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'