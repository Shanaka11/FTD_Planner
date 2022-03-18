# Python
# Django
# Rest Framework
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
# Local

class BaseApi(viewsets.ModelViewSet):

    # Show all entries
    def get_queryset_all(self):
        return self.queryset
        
    # Only show data connected to the user
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def getFilters(self, request, **kwargs):
        try:
            key_list = []
            filters = self.filterset_class.get_filters()
            for key, value in filters.items():
                key_list.append(key)
            return Response({"filters": key_list})
        except:
            return Response({"filters": []})