from planning.models import DayPlanning
from rest_framework import serializers

class DayPlanningSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DayPlanning
		fields = ('day_of_the_week', 'time')
