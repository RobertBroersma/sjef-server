from rest_framework import status
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
import json

from functional_tests.base import BaseTest
from planning.models import DayPlanning

class TestDayPlanning(BaseTest):

    #can create when logged in
    def test_can_create_dayplanning(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        data = {'day_of_the_week': 0, 'time': datetime.time(12, 0)}

        url = reverse('dayplanning-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #can read owned

    #can update owned

    #can delete owned

    #cant create when logged out
    def test_cant_create_dayplanning_when_unauthorized(self):
        data = {'day_of_the_week': 0, 'time': datetime.time(12, 0)}

        url = reverse('dayplanning-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #cant read others'

    #cant update others'

    #cant delete others'

    def test_dayplanning_associated_with_profile(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        data = {'day_of_the_week': 0, 'time': datetime.time(12, 0)}

        url = reverse('dayplanning-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, data)

        self.assertEqual(DayPlanning.objects.first().owner, user.profile)
