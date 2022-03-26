# Python
# Django
import datetime
from multiprocessing import context
from django.db.transaction import atomic
# Rest Framework
from rest_framework.decorators import action
from rest_framework.response import Response
# Base
from ftd_auth.api.baseApi import BaseApi
from planner.api.reservationApi import ReservationApi
# Local
from ..models import Activity, Reservation
from ..serializers.activitySerializer import ActivitySerializer, FullActivitySerializer
from ..filters.activityFilter import ActivityFilter

class ActivityApi(BaseApi):

    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    filterset_class = ActivityFilter

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context.update({ 'endTime': self.request.data.get('endTime') })
    #     # print(context)
    #     print(self.request.data)
    #     return context

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
        startTime = tempRequest.data.get("startTime")
        endTime = tempRequest.data.get("endTime")

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
    
    @atomic
    def update(self, request, *args, **kwargs):
        """
        request.data = {
            id: ''
            title: ''
            description: ''
            color: ''
            repeat: 'Never'
            repeatUntil: ''
        }
        """
        # Fetch Existing Record
        oldActivity = Activity.objects.get(id=request.data["id"])

        tempRequest = request
        tempRequest.data["user"] = oldActivity.user.id

        response = super().update(tempRequest, *args, **kwargs)

        if oldActivity.repeat != request.data["repeat"] or oldActivity.repeatUntil != request.data["repeatUntil"]:
            ReservationApi.regenarateReservations({
                "id": request.data["id"],
                "startTime": tempRequest.data['startTime'],
                "endTime": tempRequest.data['endTime'],
                "repeat": tempRequest.data['repeat'],
                "repeatUntil": tempRequest.data.get('repeatUntil')
            })

        return response

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
     
    @action(detail=False, methods=['get'])
    def activeList(self, request, *args, **kwargs):
        startDate = request.query_params.get("startDate")
        endDate = request.query_params.get("endDate")

        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S%z")
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S%z")

        queryset = Activity.objects.filter(user=request.user)
        queryset = queryset.filter(reservation__startTime__range=[startDate, endDate]).distinct()
        serializer = FullActivitySerializer(
            queryset, 
            many=True, 
            context={
                'startDate': startDate, 
                'endDate': endDate}
            )

        return Response(serializer.data, status=200)