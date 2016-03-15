from __future__ import unicode_literals

from django.db import models
from django.db.models import F, Func
from django.db.models.signals import post_save
from dry_rest_permissions.generics import authenticated_users
from usersettings.models import Profile
from recipes.models import Recipe
from core.models import Tag
import datetime
import random

class WeekPlanning(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile)

    def __str__(self):
        return self.name

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
    label = models.CharField(max_length=255)
    size = models.FloatField(default=1)
    owner = models.ForeignKey(Profile)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.label

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
    leftovers_from = models.ForeignKey('DayPlanning', null=True, blank=True)
    time = models.TimeField()
    week_planning = models.ForeignKey(WeekPlanning)
    owner = models.ForeignKey(Profile)

    def __str__(self):
        days_of_the_week = ['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag', 'Zondag']
        return days_of_the_week[self.day_of_the_week] + ' ' + self.meal_setting.label

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

def create_planning(sender, instance, created, **kwargs):
    if created:
        weekplanning = WeekPlanning.objects.create(name='Standaard', owner=instance)
        breakfast = MealSetting.objects.create(label='Ontbijt', owner=instance, size=2)
        lunch = MealSetting.objects.create(label='Lunch', owner=instance, size=2)
        dinner = MealSetting.objects.create(label='Dinner', owner=instance, size=3)
        snack = MealSetting.objects.create(label='Snack', owner=instance, size=1)
        for day in range(5):
            DayPlanning.objects.create(day_of_the_week=day, meal_setting=breakfast, time=datetime.time(9,0), week_planning=weekplanning, owner=instance)
            DayPlanning.objects.create(day_of_the_week=day, meal_setting=lunch, time=datetime.time(12,0), week_planning=weekplanning, owner=instance)
            DayPlanning.objects.create(day_of_the_week=day, meal_setting=snack, time=datetime.time(15,0), week_planning=weekplanning, owner=instance)
            DayPlanning.objects.create(day_of_the_week=day, meal_setting=dinner, time=datetime.time(19,0), week_planning=weekplanning, owner=instance)
            DayPlanning.objects.create(day_of_the_week=day, meal_setting=snack, time=datetime.time(22,0), week_planning=weekplanning, owner=instance)
post_save.connect(create_planning, sender=Profile)

class Meal(models.Model):
    date = models.DateField()
    recipe = models.ForeignKey(Recipe)
    day_planning = models.ForeignKey(DayPlanning)
    owner = models.ForeignKey(Profile)
    servings = models.FloatField()

    def __str__(self):
        return str(self.servings) + 'x ' + self.recipe.name

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

    @staticmethod
    def generate_mealplan(profile, energy, macros, daterange):
        plan = []

        d = daterange['start']
        delta = datetime.timedelta(days=1)
        while d <= daterange['end']:
            dayplannings = DayPlanning.objects.filter(day_of_the_week=d.weekday())
            Meal.objects.filter(date=d).delete()

            total_meal_size = dayplannings.aggregate(total_size=models.Sum('meal_setting__size'))['total_size']
            for day_planning in dayplannings:
                #TODO: Refactor to not use database level ABS?
                recipes = Recipe.objects.annotate(carbs_deviation=Func(F('carbs_relative') - macros['carbs'], function='ABS'), protein_deviation=Func(F('protein_relative') - macros['protein'], function='ABS'), fat_deviation=Func(F('fat_relative') - macros['fat'], function='ABS'), total_deviation=F('carbs_deviation') + F('protein_deviation') + F('fat_deviation')).order_by('total_deviation')[:50]

                index = int(random.expovariate(0.1))
                if index > 49:
                    index = 49

                recipe = recipes[index]
                meal = Meal.objects.create(date=d, recipe=recipe, day_planning=day_planning, owner=profile, servings=round(2 * energy / total_meal_size / recipe.energy)/2)
                plan.append(meal)
            d += delta

        return plan
