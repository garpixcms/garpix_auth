from django.test import TestCase
from django.contrib.auth.models import User


class LoginViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser1'
        self.password = '12345'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()

    def test_invalid_username_password(self):
        response = self.client.post(
            '/login/',
            {
                'username': self.username,
                'password': 'passwordtest',
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.content, b'{"__all__": ["Invalid: username / password"]}')

    def test_valid_username_password(self):
        response = self.client.post(
            '/login/',
            {
                'username': self.username,
                'password': self.password,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_valid_redirects(self):
        response = self.client.post(
            '/login/',
            {
                'username': self.username,
                'password': self.password,
            },
        )
        self.assertRedirects(response, '/')
