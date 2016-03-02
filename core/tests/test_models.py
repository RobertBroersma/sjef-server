from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import NutritionalValue
import json

class CoreTest(APITestCase):
    pass
    # def test_can_create_NutritionalValue(self):
    #     nutritional_value = NutritionalValue.objects.create(label='Calorieen', unit='kcal')
    #
    #     self.assertEqual(NutritionalValue.objects.first(), nutritional_value)
