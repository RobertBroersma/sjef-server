from dal import autocomplete
from django import forms
from recipes.models import Ingredient, IngredientTag


class IngredientForm(forms.ModelForm):
    ingredient_tag = forms.ModelChoiceField(
        queryset=IngredientTag.objects.all(),
        widget=autocomplete.ModelSelect2(url='ingredienttag-autocomplete')
    )

    class Meta:
        model = Ingredient
        fields = ('__all__')
