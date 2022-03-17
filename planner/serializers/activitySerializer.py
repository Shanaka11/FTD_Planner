# Python
# Django
# Rest Framework
from rest_framework.serializers import ModelSerializer
# Local
from ..models import Activity

class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'