from __future__ import unicode_literals

from django.db import models
from dry_rest_permissions.generics import authenticated_users
from usersettings.models import Profile

class DayPlanning(models.Model):
    day_of_the_week = models.IntegerField()
    time = models.TimeField()
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
