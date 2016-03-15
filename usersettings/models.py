from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from core.models import NutritionalValue
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        name = ''
        if (self.first_name):
            name += self.first_name
        if (self.last_name):
            name += ' ' + self.last_name
        if name == '':
            name = self.user.username

        return name

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return request.user == self.user

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.user

class DRI(models.Model):
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)
    nutritional_value = models.ForeignKey(NutritionalValue, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        DRI.objects.create(owner=profile, nutritional_value=NutritionalValue.objects.get(label='calories'), amount=4000)
        DRI.objects.create(owner=profile, nutritional_value=NutritionalValue.objects.get(label='protein'), amount=0.3)
        DRI.objects.create(owner=profile, nutritional_value=NutritionalValue.objects.get(label='carbs'), amount=0.4)
        DRI.objects.create(owner=profile, nutritional_value=NutritionalValue.objects.get(label='fat'), amount=0.3)
post_save.connect(create_profile, sender=User)
