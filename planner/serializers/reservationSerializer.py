# Python
# Django
# Rest Framework
from rest_framework.serializers import ModelSerializer, ListSerializer
# Local
from ..models import Reservation

class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        
class FilteredListSerializer(ListSerializer):
    def to_representation(self, data):
        data = data.filter(startTime__range=[self.context['startDate'], self.context['endDate']])
        return super(FilteredListSerializer, self).to_representation(data)
class ActivityReservationSerializer(ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = Reservation
        fields = ('id', 'startTime', 'endTime')