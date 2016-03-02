from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import json

class BaseTest(APITestCase):

    def create_account(self, username, password):
        return User.objects.create_user(username, None, password)

    def get_token(self, username, password):
        url = '/api-token-auth/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        if (response.status_code == status.HTTP_200_OK):
            return json.loads(response.content)['token']
        else:
            return None
