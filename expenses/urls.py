from django.urls import path

from expenses.views import TripExpenseListCreateView

urlpatterns = [
    path('trips/<uuid:trip_id>/expenses', TripExpenseListCreateView.as_view(), name='trip-expenses'),
]
