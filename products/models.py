from __future__ import unicode_literals
from django.db import models

from recipes.models import IngredientTag

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    ingredient_tags = models.ManyToManyField(IngredientTag)
    price = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    unit = models.CharField(max_length=255, default='g')

    def __str__(self):
        return self.brand + ' ' + self.name
