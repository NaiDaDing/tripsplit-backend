from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView

from expenses.models import Expense
from expenses.serializers import ExpenseSerializer
from trips.models import Trip


class TripExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_trip(self):
        return get_object_or_404(
            Trip,
            id=self.kwargs['trip_id'],
            created_by=self.request.user,
        )

    def get_queryset(self):
        return Expense.objects.filter(trip=self.get_trip())

    def perform_create(self, serializer):
        serializer.save(trip=self.get_trip(), paid_by=self.request.user)
