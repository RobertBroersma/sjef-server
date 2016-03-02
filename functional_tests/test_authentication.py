from django.core.urlresolvers import reverse
from rest_framework import status
from django.contrib.auth.models import User
from functional_tests.base import BaseTest

class FunctionalTest(BaseTest):

    def create_account(self, username, password):
        return User.objects.create_user(username, None, password)

    def test_can_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('user-list')
        data = {'username': 'piebe', 'password': 'bliksem'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'piebe')

    def test_can_get_jwt(self):
        user = self.create_account('henk', 'detank')

        url = '/api-token-auth/'
        data = {'username': 'henk', 'password': 'detank'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_login(self):
        url = '/api-token-auth/'
        data = {'username': 'notauser', 'password': 'notapassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
