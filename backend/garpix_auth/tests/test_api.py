from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import override_settings
import time


class LoginApiTest(TestCase):
    def setUp(self):
        self.username = 'testuser1'
        self.password = '12345'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()

    def test_invalid_username_password(self):
        response = self.client.post(
            reverse('garpix_auth:api_login'),
            {
                'username': self.username,
                'password': 'passwordtest',
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertDictEqual(response.json(), {"non_field_errors": ["Unable to log in with provided credentials."]})

    def test_valid_username_password(self):
        response = self.client.post(
            reverse('garpix_auth:api_login'),
            {
                'username': self.username,
                'password': self.password,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        self.assertNotEqual(response.json()['access_token'], '')
        self.assertIn('access_token_expires', response.json())
        self.assertIn('refresh_token', response.json())
        self.assertNotEqual(response.json()['refresh_token'], '')
        self.assertIn('refresh_token_expires', response.json())
        self.assertIn('token_type', response.json())

    def test_access_to_protected_view(self):
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json')
        self.assertDictEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
        # auth
        response = self.client.post(
            reverse('garpix_auth:api_login'),
            {
                'username': self.username,
                'password': self.password,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token = response.json()['access_token']
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertDictEqual(response.json(), {'username': self.username})

    def test_access_to_protected_view_after_logout(self):
        response = self.client.post(
            reverse('garpix_auth:api_login'),
            {
                'username': self.username,
                'password': self.password,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token = response.json()['access_token']
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertDictEqual(response.json(), {'username': self.username})
        # logout
        response = self.client.post(reverse('garpix_auth:api_logout'), HTTP_ACCEPT='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertDictEqual(response.json(), {'result': True})
        # get protected view after logout
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json')
        self.assertDictEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    @override_settings(GARPIX_ACCESS_TOKEN_TTL_SECONDS=5)
    def test_refresh_token(self):
        response = self.client.post(
            reverse('garpix_auth:api_login'),
            {
                'username': self.username,
                'password': self.password,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token1 = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token1}')
        self.assertDictEqual(response.json(), {'username': self.username})
        # wait and get protected view with expired access token
        time.sleep(5)
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json')
        self.assertDictEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
        # refresh token
        response = self.client.post(
            reverse('garpix_auth:api_refresh'),
            {
                'refresh_token': refresh_token,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token2 = response.json()['access_token']
        self.assertEqual(access_token1, access_token2)
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token2}')
        self.assertDictEqual(response.json(), {'username': self.username})

    @override_settings(GARPIX_REFRESH_TOKEN_TTL_SECONDS=5)
    def test_refresh_token_expired(self):
        response = self.client.post(
            reverse('garpix_auth:api_login'),
            {
                'username': self.username,
                'password': self.password,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertDictEqual(response.json(), {'username': self.username})
        # refresh token
        time.sleep(5)
        response = self.client.post(
            reverse('garpix_auth:api_refresh'),
            {
                'refresh_token': refresh_token,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'result': False})
