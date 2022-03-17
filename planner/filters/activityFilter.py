# Python
# Django
# Rest Framework
# Filters
from django_filters import rest_framework as filters
from django_filters.filters import OrderingFilter
# Local
from ..models import Activity

class ActivityFilter(filters.FilterSet):

    o = OrderingFilter(
        fields=(
            ('id', 'id'),
            ('title', 'title')
        )
    )
    class Meta:
        model = Activity
        fields = {
            'title' : ['exact', 'icontains']
        }