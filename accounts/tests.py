from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class AuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_creates_user_without_returning_password(self):
        response = self.client.post(
            '/api/auth/register',
            {
                'username': 'naida',
                'email': 'naida@example.com',
                'password': 'StrongPass123!',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'naida')
        self.assertEqual(response.data['email'], 'naida@example.com')
        self.assertNotIn('password', response.data)
        self.assertTrue(get_user_model().objects.filter(username='naida').exists())

    def test_login_returns_access_and_refresh_tokens(self):
        get_user_model().objects.create_user(
            username='naida',
            email='naida@example.com',
            password='StrongPass123!',
        )

        response = self.client.post(
            '/api/auth/login',
            {
                'username': 'naida',
                'password': 'StrongPass123!',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_returns_new_access_token(self):
        get_user_model().objects.create_user(
            username='naida',
            email='naida@example.com',
            password='StrongPass123!',
        )
        login_response = self.client.post(
            '/api/auth/login',
            {
                'username': 'naida',
                'password': 'StrongPass123!',
            },
            format='json',
        )

        response = self.client.post(
            '/api/auth/refresh',
            {'refresh': login_response.data['refresh']},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
