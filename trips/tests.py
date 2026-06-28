from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from trips.models import Trip


class TripApiTests(TestCase):
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

    def test_create_trip_requires_authentication(self):
        response = self.client.post(
            '/api/trips',
            {'name': 'Tokyo', 'base_currency': 'TWD'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_trip(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/api/trips',
            {'name': 'Tokyo', 'base_currency': 'twd'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Tokyo')
        self.assertEqual(response.data['base_currency'], 'TWD')
        trip = Trip.objects.get(id=response.data['id'])
        self.assertEqual(trip.created_by, self.user)

    def test_list_returns_only_current_users_trips(self):
        Trip.objects.create(name='Tokyo', base_currency='TWD', created_by=self.user)
        Trip.objects.create(name='Osaka', base_currency='JPY', created_by=self.other_user)
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/trips')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Tokyo')

    def test_retrieve_other_users_trip_returns_not_found(self):
        other_trip = Trip.objects.create(
            name='Osaka',
            base_currency='JPY',
            created_by=self.other_user,
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/api/trips/{other_trip.id}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
