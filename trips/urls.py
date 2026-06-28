from rest_framework.routers import DefaultRouter

from trips.views import TripViewSet

router = DefaultRouter(trailing_slash=False)
router.register('trips', TripViewSet, basename='trip')

urlpatterns = router.urls
