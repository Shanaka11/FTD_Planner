# Python
# Django
import datetime
from urllib import response
from django.db.transaction import atomic
# Rest Framework
from rest_framework.decorators import action
from rest_framework.response import Response
# Base
from ftd_auth.api.baseApi import BaseApi
from planner.api.reservationApi import ReservationApi
# Local
from ..models import Activity
from ..serializers.activitySerializer import ActivitySerializer, FullActivitySerializer
from ..filters.activityFilter import ActivityFilter

class ActivityApi(BaseApi):

    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    filterset_class = ActivityFilter

    # Only show data connected to the user
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @atomic
    def create(self, request, *args, **kwargs):
        """
        request.data = {
            title: ''
            description: ''
            color: ''
            repeat: 'Never'
            startTime: ''
            endTime: ''
            repeaUntil: ''
        }
        ** For initial requirment do not send repeat value
        ** Dates are for reservation
        """
        # Added the user from the request
        tempRequest = request
        tempRequest.data['user'] = request.user.id

        # Remove the reservation details
        startTime = tempRequest.data.pop("startTime")
        endTime = tempRequest.data.pop("endTime")

        response =  super().create(tempRequest, *args, **kwargs)
        # After creating the activity make the reservations
        
        ReservationApi.makeReservations({
            "activity": response.data["id"],
            "startTime": startTime,
            "endTime": endTime,
            "repeat": response.data['repeat'],
            "repeatUntil": response.data['repeatUntil']
        })

        return response

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        request.data = {
            title: ''
            description: ''
            color: ''
            repeat: 'Never'
            repeaUntil: ''
        }
        ** For initial requirment do not send repeat value
        ** Dates are for reservation
        """
        response = super().update(request, *args, **kwargs)
        return response

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
     
    @action(detail=False, methods=['get'])
    def activeList(self, request, *args, **kwargs):
        startDate = request.query_params.get("startDate")
        endDate = request.query_params.get("endDate")

        startDate = datetime.datetime.strptime(startDate, "%Y%m%d").date()
        endDate = datetime.datetime.strptime(endDate, "%Y%m%d").date()

        queryset = self.get_queryset().filter(reservation__startTime__range=[startDate, endDate])
        serializer = FullActivitySerializer(queryset, many=True)

        return Response(serializer.data, status=200)