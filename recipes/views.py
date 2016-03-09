from recipes.models import Recipe, IngredientTag
from rest_framework import viewsets, permissions
from recipes.serializers import RecipeSerializer, IngredientTagSerializer
from dry_rest_permissions.generics import DRYPermissions


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all().order_by()
    serializer_class = RecipeSerializer
    permission_classes = (DRYPermissions,)


class IngredientTagViewSet(viewsets.ModelViewSet):
    queryset = IngredientTag.objects.all()
    serializer_class = IngredientTagSerializer
    permission_classes = (DRYPermissions,)
