# Python
# Django
# Rest Framework
# Filters
from django_filters import rest_framework as filters
from django_filters.filters import OrderingFilter
# Local
from ..models import Reservation

class ReservationFilter(filters.FilterSet):

    o = OrderingFilter(
        fields=(
            ('startTime', 'startTime'),
            ('endTime', 'endTime')
        )
    )
    class Meta:
        model = Reservation
        fields = {
            'startTime' : ['exact', 'icontains'],
            'endTime' : ['exact', 'icontains']
        }