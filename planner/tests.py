from functools import cmp_to_key
from multiprocessing import context
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from planner.models import Activity, Reservation
from planner.serializers.activitySerializer import FullActivitySerializer
class TestPlanner(APITestCase):

    # Setup
    # 2 users
    def setUp(self):
        self.user = User.objects.create_user(username="shanakaabeysinghe@gmail.com", first_name="Shanaka", password="12345")


        # Create Activity & Reservation
        activity = Activity.objects.create(
            user = self.user,
            title = "Dummy User 1",
            description = "Dummy 1",
            color = "Red",
            repeat = "Never"
        )

        reservation = Reservation.objects.create(
            activity = activity,
            startTime = "2022-05-01T12:00:00Z",
            endTime= "2022-05-01T12:00:00Z"
        )

        self.user = User.objects.create_user(username="shanakaabeysinghe1@gmail.com", first_name="Bandara", password="12345")

        activity = Activity.objects.create(
            user = self.user,
            title = "Dummy User 2",
            description = "Dummy 2",
            color = "Blue",
            repeat = "Never"
        )

        reservation = Reservation.objects.create(
            activity = activity,
            startTime = "2022-05-01T12:00:00Z",
            endTime= "2022-05-01T12:00:00Z"
        )

        self.logFirstUser()

    def logFirstUser(self):
        data = {
            "username": "shanakaabeysinghe@gmail.com",
	        "password": "12345"
        }
        response = self.client.post("/api/user/token/", data)

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    
    # Check input validation
    def test_input_validation(self):
        # startTime > endTime
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Never",
            "startTime": "2022-06-01T14:00:00Z",
            "endTime": "2022-06-01T13:00:00Z",
        }

        self.create_activity(data, status.HTTP_400_BAD_REQUEST)

        # repeat != Never and repeatUntil is null
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Daily",
            "startTime": "2022-06-01T12:00:00Z",
            "endTime": "2022-06-01T13:00:00Z",
        }

        self.create_activity(data, status.HTTP_400_BAD_REQUEST)

        # startTime, endTime is null
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Daily"
        }

        self.create_activity(data, status.HTTP_400_BAD_REQUEST)

        # validUntl > endTime
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Daily",
            "startTime": "2022-06-01T12:00:00Z",
            "endTime": "2022-06-01T13:00:00Z",
            "repeatUntil": "2022-05-10T23:59:00Z" 
        }
        self.create_activity(data, status.HTTP_400_BAD_REQUEST)

    # Create activities for Never Daily, Weekly, Biweekly, Monthly
    def test_crud_activities(self):
        # Never
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Never",
            "startTime": "2022-06-01T12:00:00Z",
            "endTime": "2022-06-01T13:00:00Z",
        }

        self.create_activity(data, status.HTTP_201_CREATED)

        # Daily
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Daily",
            "startTime": "2022-07-01T12:00:00Z",
            "endTime": "2022-07-01T13:00:00Z",
            "repeatUntil": "2022-07-10T23:59:00Z" 
        }

        self.create_activity(data, status.HTTP_201_CREATED)

        # Weekly
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Weekly",
            "startTime": "2022-08-01T12:00:00Z",
            "endTime": "2022-08-01T13:00:00Z",
            "repeatUntil": "2022-08-30T23:59:00Z" 
        }

        self.create_activity(data, status.HTTP_201_CREATED)

        # Biweekly
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Biweekly",
            "startTime": "2022-09-01T12:00:00Z",
            "endTime": "2022-09-01T13:00:00Z",
            "repeatUntil": "2022-09-30T23:59:00Z" 
        }

        self.create_activity(data, status.HTTP_201_CREATED)

        # Biweekly
        data = {
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Monthly",
            "startTime": "2022-10-01T12:00:00Z",
            "endTime": "2022-10-01T13:00:00Z",
            "repeatUntil": "2022-11-30T23:59:00Z" 
        }

        self.create_activity(data, status.HTTP_201_CREATED)

        # Check getActiveReservations endpoint
        self.fetch_active_reservations('2022-06-01T12:00:00Z', '2022-06-30T12:00:00Z', 1)
        self.fetch_active_reservations('2022-07-01T12:00:00Z', '2022-07-30T12:00:00Z', 10)
        self.fetch_active_reservations('2022-07-01T12:00:00Z', '2022-07-08T12:00:00Z', 8)
        self.fetch_active_reservations('2022-08-01T12:00:00Z', '2022-08-30T12:00:00Z', 5)
        self.fetch_active_reservations('2022-09-01T12:00:00Z', '2022-09-30T12:00:00Z', 3)
        self.fetch_active_reservations('2022-10-01T12:00:00Z', '2022-12-30T12:00:00Z', 2)

        # Update Activity

        data = {
            "id": "4",
            "title": "Test User 1",
            "description": "Test User 1",
            "color": "Red",
            "repeat": "Weekly",
            "startTime": "2022-07-01T12:00:00Z",
            "endTime": "2022-07-01T13:00:00Z",
            "repeatUntil": "2022-07-20T23:59:00Z" 
        }

        self.update_activity(data, status.HTTP_200_OK)
        self.fetch_active_reservations('2022-07-01T12:00:00Z', '2022-07-30T12:00:00Z', 3)

        # Delete Activity
        self.remove_activity('4')
        self.fetch_active_reservations('2022-07-01T12:00:00Z', '2022-07-30T12:00:00Z', 0)
        
    # Check if only the related activities are fetched when using the retrive, list end points
    def test_list(self):
        response = self.client.get("/api/planner/activity/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrive(self):

        response = self.client.get("/api/planner/activity/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/api/planner/activity/2/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def create_activity (self, data, status):
        response = self.client.post("/api/planner/activity/", data, format='json')
        self.assertEqual(response.status_code, status)
        return response

    def update_activity (self, data, status):
        response = self.client.put("/api/planner/activity/4/", data, format='json', follow=True)
        self.assertEqual(response.status_code, status)
        return response

    def remove_activity (self, id):
        response = self.client.delete("/api/planner/activity/" + id + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def fetch_active_reservations (self, startDate, endDate, count):
        response = self.client.get("/api/planner/activity/activeList?startDate=" + startDate + "&endDate=" + endDate, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        activities = Activity.objects.filter(user__id = '1')
        activities = activities.filter(reservation__startTime__range=[startDate, endDate]).distinct()
        reservationCount = Reservation.objects.filter(activity__in = activities)
        reservationCount = reservationCount.filter(startTime__range = [startDate, endDate]).count()
        
        self.assertEqual(reservationCount, count)

        serializer = FullActivitySerializer(
            activities, 
            many=True, 
            context={
                'startDate': startDate, 
                'endDate': endDate
            })

        self.assertEqual(serializer.data, response.data)

