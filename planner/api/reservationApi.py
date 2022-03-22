# Python
# Django
from calendar import month
from dateutil.relativedelta import relativedelta
import datetime
# Rest Framework
from rest_framework.decorators import action
from rest_framework.response import Response
# Base
from ftd_auth.api.baseApi import BaseApi
# Local
from ..models import Reservation
from ..serializers.reservationSerializer import ReservationSerializer
from ..filters.reservationFilter import ReservationFilter
from ..enums import Repeat

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
        tempStart = reservationData["startTime"]
        tempEnd = reservationData["endTime"]
        repeat = reservationData["repeat"]
        repeatUntil = datetime.datetime.strptime(reservationData["repeatUntil"],'%Y-%m-%dT%H:%M:%S%z')

        def makeReservation(data, increment):
            tempStart = datetime.datetime.strptime(data["startTime"], '%Y-%m-%dT%H:%M:%S%z')
            tempEnd = datetime.datetime.strptime(data["endTime"], '%Y-%m-%dT%H:%M:%S%z')
            

            while(tempEnd < repeatUntil):
                data["startTime"] = tempStart
                data["endTime"] = tempEnd

                serializer = ReservationSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                if increment > 29:
                    tempStart = tempStart + relativedelta(months = 1)
                    tempEnd = tempEnd + relativedelta(months = 1)
                else:
                    tempStart = tempStart + datetime.timedelta(days=increment)
                    tempEnd = tempEnd + datetime.timedelta(days=increment)

        if(repeat == Repeat.NEVER):
            tempData = {
                "activity" : reservationData["activity"],
                "startTime" : tempStart,
                "endTime" : tempEnd
            }
            serializer = ReservationSerializer(data=tempData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        else:
            tempData = {
                "activity": reservationData["activity"],
                "startTime": tempStart,
                "endTime": tempEnd
            }
            if repeat == Repeat.DAILY:
                makeReservation(tempData, 1)
            elif repeat == Repeat.WEEKLY:
                makeReservation(tempData, 7)
            elif repeat == Repeat.BIWEEKLY:
                makeReservation(tempData, 14)
            elif repeat == Repeat.MONTHLY:
                makeReservation(tempData, 30)

    # Remove Reservations on Date Range