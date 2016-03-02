from rest_framework import status
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import json

from functional_tests.base import BaseTest

class TestProfile(BaseTest):

    def test_can_create_profile(self):
        user = self.create_account('Henk', 'vries')

        self.assertIsNotNone(user.profile)

    def test_can_view_profile(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')

        url = reverse('profile-detail', args=(user.profile.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_profile_owned(self):
        user = self.create_account('Jan', 'password')
        token = self.get_token('Jan', 'password')

        url = reverse('profile-detail', args=(user.profile.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(url, {'first_name': 'John', 'last_name': 'Niks'}, format='json')
        user.profile.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        self.assertEqual(user.profile.first_name, 'John')

    #profile list only returns self
    def test_profile_list_only_returns_self(self):
        user = self.create_account('Jan', 'password')
        otheruser = self.create_account('Other', 'user')
        token = self.get_token('Jan', 'password')

        url = reverse('profile-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], user.profile.__dict__['id'], response)

    #cant view profile others'
    def test_cant_view_profile_thats_not_mine(self):
        user = self.create_account('Willem', 'Bliksem')
        otheruser = self.create_account('Berend', 'Tester')
        token = self.get_token('Willem', 'Bliksem')

        url = reverse('profile-detail', args=(otheruser.profile.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #cant update profiles of others

    #cant delete profile

    def test_unauthenticated_profile_view(self):
        user = self.create_account('Henk', 'Tester')

        url = reverse('profile-detail', args=(user.profile.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
