from rest_framework import status
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
import json

from functional_tests.base import BaseTest
from planning.models import DayPlanning, MealSetting

class TestDayPlanning(BaseTest):

    #
    # LIST
    #
    def test_can_get_list_of_owned_dayplannings(self):
        user = self.create_account('Piebe', 'Bliksem')
        otheruser = self.create_account('Henk', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        DayPlanning.objects.create(owner=user.profile, day_of_the_week=1, time=datetime.time(12, 0))
        DayPlanning.objects.create(owner=otheruser.profile, day_of_the_week=1, time=datetime.time(12, 0))

        url = reverse('dayplanning-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)
        results = json.loads(response.content)['results']

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['owner'], user.profile.__dict__['id'], response)

    def test_cant_get_list_when_logged_out(self):
        url = reverse('dayplanning-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #
    # CREATE
    #
    def test_can_create_dayplanning(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        data = {'day_of_the_week': 0, 'time': datetime.time(12, 0)}

        url = reverse('dayplanning-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)

    def test_cant_create_dayplanning_when_unauthorized(self):
        data = {'day_of_the_week': 0, 'time': datetime.time(12, 0)}

        url = reverse('dayplanning-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #
    # RETRIEVE
    #
    def test_can_get_dayplanning(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        dayplanning = DayPlanning.objects.create(owner=user.profile, day_of_the_week=1, time=datetime.time(12, 0))

        url = reverse('dayplanning-detail', args=(dayplanning.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_get_dayplannings_when_logged_out(self):
        user = self.create_account('Piebe', 'Bliksem')
        dayplanning = DayPlanning.objects.create(owner=user.profile, day_of_the_week=1, time=datetime.time(12, 0))

        url = reverse('dayplanning-detail', args=(dayplanning.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_get_dayplannings_not_owned(self):
        user = self.create_account('Piebe', 'Bliksem')
        otheruser = self.create_account('Henk', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        dayplanning = DayPlanning.objects.create(owner=otheruser.profile, day_of_the_week=1, time=datetime.time(12, 0))

        url = reverse('dayplanning-detail', args=(dayplanning.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #
    # UPDATE / PARTIAL_UPDATE
    #
    def test_can_update_owned_dayplanning(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        dayplanning = DayPlanning.objects.create(owner=user.profile, day_of_the_week=0, time=datetime.time(12,0))
        data = {'day_of_the_week': 2}

        url = reverse('dayplanning-detail', args=(dayplanning.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(url, data)
        dayplanning.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        self.assertEqual(dayplanning.day_of_the_week, 2)

    def test_cant_update_not_owned_dayplanning(self):
        user = self.create_account('Piebe', 'Bliksem')
        otheruser = self.create_account('Henk', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        dayplanning = DayPlanning.objects.create(owner=otheruser.profile, day_of_the_week=0, time=datetime.time(12,0))
        data = {'day_of_the_week': 2}

        url = reverse('dayplanning-detail', args=(dayplanning.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.patch(url, data)
        dayplanning.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(dayplanning.day_of_the_week, 0)

    #
    # DESTROY
    #
    def test_can_delete_owned_dayplanning(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        dayplanning = DayPlanning.objects.create(owner=user.profile, day_of_the_week=0, time=datetime.time(12,0))

        url = reverse('dayplanning-detail', args=(dayplanning.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response)

    def test_cant_delete_not_owned_dayplanning(self):
        user = self.create_account('Piebe', 'Bliksem')
        otheruser = self.create_account('Henk', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        dayplanning = DayPlanning.objects.create(owner=otheruser.profile, day_of_the_week=0, time=datetime.time(12,0))

        url = reverse('dayplanning-detail', args=(dayplanning.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestMealSetting(BaseTest):

    #
    # LIST
    #
    def test_can_get_list_of_owned_mealsettings(self):
        user = self.create_account('Piebe', 'Bliksem')
        otheruser = self.create_account('Henk', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        MealSetting.objects.create(owner=user.profile)
        MealSetting.objects.create(owner=otheruser.profile)

        url = reverse('mealsetting-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)
        results = json.loads(response.content)['results']

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['owner'], user.profile.__dict__['id'], response)

    def test_cant_get_list_when_logged_out(self):
        url = reverse('mealsetting-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #
    # CREATE
    #
    def test_can_create_mealsetting(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        data = {'size': 2}

        url = reverse('mealsetting-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)
        self.assertEqual(MealSetting.objects.first().size, 2)

    def test_cant_create_mealsetting_when_unauthorized(self):
        data = {'size': 4}

        url = reverse('mealsetting-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #
    # RETRIEVE
    #
    def test_can_get_owned_mealsetting(self):
        user = self.create_account('Piebe', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        mealsetting = MealSetting.objects.create(owner=user.profile, size=2)

        url = reverse('mealsetting-detail', args=(mealsetting.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_get_mealsetting_when_logged_out(self):
        user = self.create_account('Piebe', 'Bliksem')
        mealsetting = MealSetting.objects.create(owner=user.profile, size=2)

        url = reverse('mealsetting-detail', args=(mealsetting.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_get_mealsettings_not_owned(self):
        user = self.create_account('Piebe', 'Bliksem')
        otheruser = self.create_account('Henk', 'Bliksem')
        token = self.get_token('Piebe', 'Bliksem')
        mealsetting = MealSetting.objects.create(owner=otheruser.profile, size=6)

        url = reverse('mealsetting-detail', args=(mealsetting.id,))
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #
    # UPDATE / PARTIAL_UPDATE
    #
    def test_can_update_owned_mealsetting(self):
        pass

    def test_cant_update_not_owned_mealsetting(self):
        pass

    #
    # DESTROY
    #
    def test_can_delete_owned_mealsetting(self):
        pass

    def test_cant_delete_not_owned_mealsetting(self):
        pass
