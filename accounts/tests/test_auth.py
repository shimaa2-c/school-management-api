from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='student1',
            email='student@example.com',
            password='Student123!',
            role='student',
        )

    def test_login_valid_credentials(self):
        response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'student1',
                'password': 'Student123!',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            'access',
            response.data,
        )

        self.assertIn(
            'refresh',
            response.data,
        )

    def test_login_wrong_password(self):
        response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'student1',
                'password': 'WrongPassword!',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_protected_endpoint_requires_authentication(self):
        response = self.client.get(
            '/api/auth/me/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_me_returns_current_user(self):
        login_response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'student1',
                'password': 'Student123!',
            },
            format='json',
        )

        access_token = login_response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        response = self.client.get(
            '/api/auth/me/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data['data']['username'],
            'student1',
        )
    def test_refresh_token_works(self):
        login_response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'student1',
                'password': 'Student123!',
            },
            format='json',
        )

        refresh_token = login_response.data['refresh']

        response = self.client.post(
            '/api/auth/token/refresh/',
            {
                'refresh': refresh_token,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            'access',
            response.data,
        )
    def test_logout_blacklists_refresh_token(self):
        login_response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'student1',
                'password': 'Student123!',
            },
            format='json',
        )

        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        logout_response = self.client.post(
            '/api/auth/logout/',
            {
                'refresh': refresh_token,
            },
            format='json',
        )

        self.assertEqual(
            logout_response.status_code,
            status.HTTP_200_OK,
        )

        refresh_response = self.client.post(
            '/api/auth/token/refresh/',
            {
                'refresh': refresh_token,
            },
            format='json',
        )

        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    def test_change_password(self):
        login_response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'student1',
                'password': 'Student123!',
            },
            format='json',
        )

        access_token = login_response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        response = self.client.post(
            '/api/auth/change-password/',
            {
                'old_password': 'Student123!',
                'new_password': 'NewStudent123!',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password('NewStudent123!')
        )
    def test_change_password_with_wrong_old_password(self):
        login_response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'student1',
                'password': 'Student123!',
            },
            format='json',
        )

        access_token = login_response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        response = self.client.post(
            '/api/auth/change-password/',
            {
                'old_password': 'WrongPassword!',
                'new_password': 'NewStudent123!',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
