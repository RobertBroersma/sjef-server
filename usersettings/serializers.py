from usersettings.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Profile
		fields = ('url', 'id', 'user', 'first_name', 'last_name')
