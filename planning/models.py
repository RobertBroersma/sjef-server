from __future__ import unicode_literals

from django.db import models
from dry_rest_permissions.generics import authenticated_users
from usersettings.models import Profile
from recipes.models import Recipe
from core.models import Tag

class WeekPlanning(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile)

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return request.user.profile == self.owner

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user.profile == self.owner

class MealSetting(models.Model):
    size = models.FloatField(default=1)
    owner = models.ForeignKey(Profile)
    tags = models.ManyToManyField(Tag)

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return request.user.profile == self.owner

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user.profile == self.owner

class DayPlanning(models.Model):
    day_of_the_week = models.IntegerField()
    meal_setting = models.ForeignKey(MealSetting)
    leftovers_from = models.ForeignKey('DayPlanning', null=True)
    time = models.TimeField()
    week_planning = models.ForeignKey(WeekPlanning)
    owner = models.ForeignKey(Profile)

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return request.user.profile == self.owner

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user.profile == self.owner

class Meal(models.Model):
    date_and_time = models.DateTimeField()
    recipe = models.ForeignKey(Recipe)
    day_planning = models.ForeignKey(DayPlanning)
    owner = models.ForeignKey(Profile)
