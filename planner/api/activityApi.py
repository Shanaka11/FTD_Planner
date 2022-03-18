# Python
# Django
# Rest Framework
from rest_framework.decorators import action
from rest_framework.response import Response
# Base
from ftd_auth.api.baseApi import BaseApi
# Local
from ..models import Activity
from ..serializers.activitySerializer import ActivitySerializer
from ..filters.activityFilter import ActivityFilter

class ActivityApi(BaseApi):

    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    filterset_class = ActivityFilter

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # After creating the activity make the reservations
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)