from __future__ import unicode_literals

from django.db import models
from dry_rest_permissions.generics import authenticated_users, allow_staff_or_superuser
from core.models import Tag, NutritionalValue
from usersettings.models import Profile
from django.db.models.signals import pre_save

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
    ingredient_tag = models.ForeignKey(IngredientTag, on_delete=models.CASCADE, related_name='ingredients')
    amount = models.FloatField()
    unit = models.CharField(max_length=255)

    def __str__(self):
        return (str(self.amount) + self.unit + ' ' + self.ingredient_tag.label).encode('ascii', 'replace')

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

class RecipeNutrition(models.Model):
    nutritional_value = models.ForeignKey(NutritionalValue, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return str(self.amount) + ' ' + self.nutritional_value.unit

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    cook_time = models.FloatField()
    source_url = models.URLField()
    source_img = models.URLField()
    ingredients = models.ManyToManyField(IngredientTag, through=Ingredient)
    tags = models.ManyToManyField(Tag, blank=True)
    nutritions = models.ManyToManyField(NutritionalValue, through=RecipeNutrition)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    energy = models.FloatField()
    protein_relative = models.FloatField()
    carbs_relative = models.FloatField()
    fat_relative = models.FloatField()

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

# def calculate_nutrition(sender, instance, **kwargs):
#     energy = instance.recipenutrition_set.get(nutritional_value__label='calories').amount
#     protein = instance.recipenutrition_set.get(nutritional_value__label='protein').amount
#     carbs = instance.recipenutrition_set.get(nutritional_value__label='carbs').amount
#     fat = instance.recipenutrition_set.get(nutritional_value__label='fat').amount
#
#     if energy > 0:
#         instance.energy = energy
#         instance.protein_relative = 4 * protein / energy
#         instance.carbs_relative = 4 * carbs / energy
#         instance.fat_relative = 4 * fat / energy
#
# pre_save.connect(calculate_nutrition, sender=Recipe)