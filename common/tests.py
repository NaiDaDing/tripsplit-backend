from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIClient


class HealthEndpointTests(SimpleTestCase):
    def test_healthz_returns_demo_message_without_authentication(self):
        response = APIClient().get('/healthz')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'status': 'ok', 'message': 'Hello CI/CD'},
        )
