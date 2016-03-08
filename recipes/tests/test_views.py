from rest_framework import status
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
import json

from functional_tests.base import BaseTest
from recipes.models import Recipe

class TestRecipe(BaseTest):

    #
    # LIST
    #
    def test_can_get_list_of_all_recipes(self):
        url = reverse('recipe-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    # CREATE
    #
    def test_can_create_recipe_when_logged_in(self):
        pass

    def test_cant_create_recipe_when_logged_out(self):
        pass
    #
    # RETRIEVE
    #
    def test_can_get_single_recipe(self):
        pass

    #
    # UPDATE / PARTIAL_UPDATE
    #
    def test_can_update_owned_recipe(self):
        pass

    def test_cant_update_not_owned_recipe(self):
        pass

    #
    # DESTROY
    #
    def test_can_delete_owned_recipe(self):
        pass

    def test_cant_delete_not_owned_recipe(self):
        pass
