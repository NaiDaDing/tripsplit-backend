from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from expenses.models import Expense
from trips.models import Trip


class ExpenseApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='naida',
            email='naida@example.com',
            password='StrongPass123!',
        )
        self.other_user = get_user_model().objects.create_user(
            username='other',
            email='other@example.com',
            password='StrongPass123!',
        )
        self.trip = Trip.objects.create(
            name='Tokyo',
            base_currency='JPY',
            created_by=self.user,
        )
        self.other_trip = Trip.objects.create(
            name='Osaka',
            base_currency='JPY',
            created_by=self.other_user,
        )

    def test_create_expense_requires_authentication(self):
        response = self.client.post(
            f'/api/trips/{self.trip.id}/expenses',
            {'title': 'Dinner', 'amount': '1200.00'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_create_expense(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f'/api/trips/{self.trip.id}/expenses',
            {'title': 'Dinner', 'amount': '1200.00'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Dinner')
        self.assertEqual(Decimal(response.data['amount']), Decimal('1200.00'))
        expense = Expense.objects.get(id=response.data['id'])
        self.assertEqual(expense.trip, self.trip)
        self.assertEqual(expense.paid_by, self.user)

    def test_user_cannot_create_expense_for_another_users_trip(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f'/api/trips/{self.other_trip.id}/expenses',
            {'title': 'Hotel', 'amount': '5000.00'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Expense.objects.count(), 0)

    def test_list_returns_only_expenses_for_trip(self):
        Expense.objects.create(
            trip=self.trip,
            title='Dinner',
            amount=Decimal('1200.00'),
            paid_by=self.user,
        )
        another_trip = Trip.objects.create(
            name='Seoul',
            base_currency='KRW',
            created_by=self.user,
        )
        Expense.objects.create(
            trip=another_trip,
            title='Taxi',
            amount=Decimal('300.00'),
            paid_by=self.user,
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/api/trips/{self.trip.id}/expenses')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Dinner')

    def test_list_expenses_for_another_users_trip_returns_not_found(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/api/trips/{self.other_trip.id}/expenses')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
