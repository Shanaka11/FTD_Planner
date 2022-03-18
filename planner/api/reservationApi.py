# Python
# Django
# Rest Framework
from venv import create
from rest_framework.decorators import action
from rest_framework.response import Response
# Base
from ftd_auth.api.baseApi import BaseApi
# Local
from ..models import Reservation
from ..serializers.reservationSerializer import ReservationSerializer
from ..filters.reservationFilter import ReservationFilter

class ReservationApi(BaseApi):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filterset_class = ReservationFilter

    # Only show data connected to the user
    def get_queryset(self):
        return self.queryset.filter(activity__user=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # Make Reservations
    def makeReservations(reservationData):
        # Make Reservations & Handle Overlaps
        temp_data = {
            "activity" : reservationData["activity"],
            "startTime" : reservationData["startTime"],
            "endTime" : reservationData["endTime"]
        }
        serializer = ReservationSerializer(data=temp_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # Remove Reservations on Date Range