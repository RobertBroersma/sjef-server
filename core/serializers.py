from django.contrib.auth.models import User
from core.models import NutritionalValue, Tag
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'password', 'first_name', 'last_name')
        write_only_fields = ('password',)
        password = serializers.CharField(
            style={'input_type': 'password'}
        )

	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
		)

		user.set_password(validated_data['password'])
		user.save()

		return user

class NutritionalValueSerializer(serializers.ModelSerializer):
	class Meta:
		model = NutritionalValue
		fields = ('label', 'unit')

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('id', 'label',)
