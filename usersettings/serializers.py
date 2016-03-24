from usersettings.models import Profile, DRI
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('id', 'dri_set', 'user')
		depth = 2

class DRISerliazer(serializers.ModelSerializer):
	class Meta:
		model = DRI
		fields = ('nutritional_value', 'amount')
