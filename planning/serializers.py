from planning.models import DayPlanning, MealSetting, Meal
from rest_framework import serializers

class DayPlanningSerializer(serializers.ModelSerializer):
	class Meta:
		model = DayPlanning
		fields = ('id', 'day_of_the_week', 'time', 'owner')
		read_only_fields = ('owner',)


class MealSettingSerializer(serializers.ModelSerializer):
	class Meta:
		model = MealSetting
		fields = ('id', 'url', 'owner', 'size')
		read_only_fields = ('owner',)


class MealSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meal
		fields = ('date', 'recipe', 'day_planning', 'servings')
		depth = 1
