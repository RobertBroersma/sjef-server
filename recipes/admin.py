from django.contrib import admin
from recipes.models import Recipe, Ingredient, IngredientTag, RecipeNutrition
from recipes.forms import IngredientForm

class IngredientInline(admin.TabularInline):
    model = Ingredient
    form = IngredientForm
    extra = 1

class NutritionsInline(admin.TabularInline):
    model = RecipeNutrition
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline, NutritionsInline)
    list_filter = ('owner',)

class IngredientTagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientTag, IngredientTagAdmin)
