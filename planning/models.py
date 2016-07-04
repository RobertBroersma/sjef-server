from __future__ import unicode_literals

from django.db import models
from django.db.models import F, Func, Count
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
    cook_time = models.FloatField(default=15)
    max_ingredients = models.IntegerField(default=0) # 0 = unlimited

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
    leftovers_from = models.ForeignKey('DayPlanning', null=True, blank=True, related_name='extra_for')
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

    def swap(self):
        #TODO: Base numbers on aggregated dayplannings / current plan?
        meal_size = self.day_planning.meal_setting.size
        meal_tags = list(self.day_planning.meal_setting.tags.values_list('id', flat=True))
        cook_time = self.day_planning.meal_setting.cook_time
        current_energy = self.recipe.energy * self.servings

        meal_rel_carbs = self.recipe.carbs_relative
        meal_rel_protein = self.recipe.protein_relative
        meal_rel_fat = self.recipe.fat_relative

        recipes = Recipe.objects
        if len(meal_tags) > 0:
            recipes = recipes.filter(tags__in=meal_tags)

        recipes = recipes.filter(owner__user__username='robert').filter(cook_time__lte=cook_time).annotate(carbs_deviation=Func(F('carbs_relative') - meal_rel_carbs, function='ABS'), protein_deviation=Func(F('protein_relative') - meal_rel_protein, function='ABS'), fat_deviation=Func(F('fat_relative') - meal_rel_fat, function='ABS'), total_deviation=F('carbs_deviation') + F('protein_deviation') + F('fat_deviation')).order_by('total_deviation')[:50]

        index = int(random.expovariate(0.2))
        if index > recipes.count():
            index = recipes.count() - 1

        recipe = recipes[index]

        self.recipe = recipe
        if current_energy > 0:
            self.servings = round(2 * current_energy / recipe.energy)/2
        else:
            self.servings = 1
        self.save()

        return self

    @staticmethod
    def generate_mealplan(profile, energy, macros, daterange):
        plan = []

        d = daterange['start']
        delta = datetime.timedelta(days=1)
        while d <= daterange['end']:
            Meal.objects.filter(date=d).delete()
            dayplannings = DayPlanning.objects.filter(day_of_the_week=d.weekday(), owner=profile).order_by('leftovers_from', '?')
            total_meal_size = dayplannings.aggregate(total_size=models.Sum('meal_setting__size'))['total_size']

            desired_kcal_from_carbs = macros['carbs'] * energy
            desired_kcal_from_protein = macros['protein'] * energy
            desired_kcal_from_fat = macros['fat'] * energy

            for day_planning in dayplannings:
                meal_size = day_planning.meal_setting.size
                meal_tags = list(day_planning.meal_setting.tags.values_list('id', flat=True))
                cook_time = day_planning.meal_setting.cook_time
                max_ingredients = day_planning.meal_setting.max_ingredients
                current_kcal_from = Meal.get_current_kcal_from(plan)

                meal_kcal_from_carbs = desired_kcal_from_carbs - current_kcal_from['carbs']
                meal_kcal_from_protein = desired_kcal_from_protein - current_kcal_from['protein']
                meal_kcal_from_fat = desired_kcal_from_fat - current_kcal_from['fat']
                meal_kcal_total_desired = meal_kcal_from_carbs + meal_kcal_from_protein + meal_kcal_from_fat

                meal_rel_carbs = meal_kcal_from_carbs / meal_kcal_total_desired
                meal_rel_protein = meal_kcal_from_protein / meal_kcal_total_desired
                meal_rel_fat = meal_kcal_from_fat / meal_kcal_total_desired

                if day_planning.leftovers_from:
                    leftover_meal = Meal.objects.filter(day_planning=day_planning.leftovers_from, date__lte=d).order_by('-date').first()
                    recipe = leftover_meal.recipe
                else:
                    if len(plan) <= 0:
                        recipes = Recipe.objects

                        # TODO: remove hotfix with meal_tags empty
                        if len(meal_tags) > 0:
                            recipes = recipes.filter(tags__in=meal_tags)

                        recipes = recipes.filter(cook_time__lte=cook_time).annotate(total_ingredients=Count('ingredients')).filter(total_ingredients__lte=max_ingredients).order_by('?')[:50]
                    else:
                        recipes = Recipe.objects
                        if len(meal_tags) > 0:
                            recipes = recipes.filter(tags__in=meal_tags)

                        recipes = recipes.filter(cook_time__lte=cook_time)
                        recipes = recipes.annotate(carbs_deviation=Func(F('carbs_relative') - meal_rel_carbs, function='ABS'), protein_deviation=Func(F('protein_relative') - meal_rel_protein, function='ABS'), fat_deviation=Func(F('fat_relative') - meal_rel_fat, function='ABS'), total_deviation=F('carbs_deviation') + F('protein_deviation') + F('fat_deviation'), total_ingredients=Count('ingredients'))
                        recipes = recipes.filter(total_ingredients__lte=max_ingredients)
                        recipes = recipes.order_by('total_deviation')[:50]

                    index = int(random.expovariate(0.5))
                    if index >= recipes.count():
                        index = recipes.count() - 1

                    recipe = recipes[index]

                meal = Meal.objects.create(date=d, recipe=recipe, day_planning=day_planning, owner=profile, servings=round(2 * meal_size * energy / total_meal_size / recipe.energy)/2)
                plan.append(meal)
            d += delta

        return plan

    @staticmethod
    def get_current_kcal_from(plan):
        macros = {
            'carbs': 0,
            'protein': 0,
            'fat': 0,
        }

        if (len(plan) <= 0):
            return macros

        for meal in plan:
            macros['carbs'] += meal.recipe.carbs_relative * meal.recipe.energy * meal.servings
            macros['protein'] += meal.recipe.protein_relative * meal.recipe.energy * meal.servings
            macros['fat'] += meal.recipe.fat_relative * meal.recipe.energy * meal.servings

        return macros
