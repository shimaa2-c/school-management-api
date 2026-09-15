from rest_framework import status
from rest_framework.test import APITestCase


class MiddlewareTests(APITestCase):

    def test_response_contains_request_id(self):
        response = self.client.get(
            '/api/auth/me/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertIn(
            'X-Request-ID',
            response,
        )

        self.assertTrue(
            response['X-Request-ID']
        )

    def test_supplied_request_id_is_preserved(self):
        request_id = 'TEST-REQUEST-123'

        response = self.client.get(
            '/api/auth/me/',
            HTTP_X_REQUEST_ID=request_id,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response['X-Request-ID'],
            request_id,
        )