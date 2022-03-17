# Python
# Django
# Rest Framework
from rest_framework.serializers import ModelSerializer
# Local
from ..models import Reservation


class ReservationSerializer(ModelSerializer):
    class Meta:
        models = Reservation