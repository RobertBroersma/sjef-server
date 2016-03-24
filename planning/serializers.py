from planning.models import DayPlanning, MealSetting, Meal, WeekPlanning
from rest_framework import serializers
from recipes.serializers import RecipeSerializer

class DayPlanningSerializer(serializers.ModelSerializer):
	week_planning_id = serializers.PrimaryKeyRelatedField(queryset=WeekPlanning.objects.all(), source='week_planning', write_only=True)
	meal_setting_id = serializers.PrimaryKeyRelatedField(queryset=MealSetting.objects.all(), source='meal_setting', write_only=True)

	class Meta:
		model = DayPlanning
		fields = ('id', 'day_of_the_week', 'time', 'meal_setting', 'week_planning', 'week_planning_id', 'meal_setting_id')
		read_only_fields = ('week_planning', 'meal_setting')
		depth = 1


class WeekPlanningSerializer(serializers.ModelSerializer):
	dayplannings = DayPlanningSerializer(source='dayplanning_set', many=True)

	class Meta:
		model = WeekPlanning
		fields = ('id', 'name', 'dayplannings')
		depth = 2


class MealSettingSerializer(serializers.ModelSerializer):
	class Meta:
		model = MealSetting
		fields = ('id', 'label', 'owner', 'size')
		read_only_fields = ('owner',)


class MealSerializer(serializers.ModelSerializer):
	recipe = RecipeSerializer()

	class Meta:
		model = Meal
		fields = ('date', 'recipe', 'day_planning', 'servings')
		depth = 2
