from django.contrib import admin
from recipes.models import Recipe, Ingredient, RecipeNutrition

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class NutritionsInline(admin.TabularInline):
    model = RecipeNutrition
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline, NutritionsInline)

admin.site.register(Recipe, RecipeAdmin)
