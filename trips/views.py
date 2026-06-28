from rest_framework.viewsets import ModelViewSet

from trips.models import Trip
from trips.serializers import TripSerializer


class TripViewSet(ModelViewSet):
    serializer_class = TripSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return Trip.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
