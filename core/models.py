from __future__ import unicode_literals

from django.db import models

class NutritionalValue(models.Model):
    label = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    def __str__(self):
        return self.label.encode('ascii', 'replace')

class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label.encode('ascii', 'replace')
