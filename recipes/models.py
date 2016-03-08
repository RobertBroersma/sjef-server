from __future__ import unicode_literals

from django.db import models
from dry_rest_permissions.generics import authenticated_users, allow_staff_or_superuser
from core.models import Tag, NutritionalValue
from usersettings.models import Profile

class IngredientTag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label.encode('ascii', 'replace')

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(request):
        return False


class Ingredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient_tag = models.ForeignKey(IngredientTag, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=255)

    def __str__(self):
        return (str(self.amount) + self.unit + ' ' + self.ingredient_tag.label).encode('ascii', 'replace')


class RecipeNutrition(models.Model):
    nutritional_value = models.ForeignKey(NutritionalValue, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return str(self.amount) + ' ' + self.nutritional_value.unit

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(IngredientTag, through=Ingredient)
    tags = models.ManyToManyField(Tag, blank=True)
    nutritions = models.ManyToManyField(NutritionalValue, through=RecipeNutrition)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name.encode('ascii', 'replace')

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user.profile == self.owner
