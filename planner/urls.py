# Python
# Django
from django.urls import path, include
# Rest Framework
from rest_framework.routers import DefaultRouter
# Local
from .api.activityApi import ActivityApi
from .api.reservationApi import ReservationApi

router = DefaultRouter()
router.register('activity', ActivityApi)
router.register('reservation', ReservationApi)

urlpatterns = [
    path('', include(router.urls))
]