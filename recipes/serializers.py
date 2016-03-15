from recipes.models import Recipe, IngredientTag, Ingredient, RecipeNutrition
from rest_framework import serializers

from core.serializers import NutritionalValueSerializer

class IngredientTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = IngredientTag
		fields = ('id', 'label')

class IngredientSerializer(serializers.ModelSerializer):

	class Meta:
		model = Ingredient
		fields = ('amount', 'unit', 'ingredient_tag')
		depth = 1

class NutritionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = RecipeNutrition
		fields = ('amount', 'nutritional_value')
		depth = 1

class RecipeSerializer(serializers.ModelSerializer):
	ingredients = IngredientSerializer(source='ingredient_set', many=True)
	nutritions = NutritionsSerializer(source='recipenutrition_set', many=True)

	class Meta:
		model = Recipe
		fields = ('id', 'url', 'name', 'ingredients', 'tags', 'nutritions', 'owner')
		read_only_fields = ('owner',)
		depth = 2
