from recipes.models import Recipe, IngredientTag, Ingredient
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from recipes.serializers import RecipeSerializer, IngredientTagSerializer, IngredientSerializer
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.decorators import list_route
from django.db.models import Sum, F


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


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (DRYPermissions,)

    @list_route(methods=['get'])
    def get_groceries(self, request):
        ingredients = Ingredient.objects.filter(recipe__meal__owner=request.user.profile).annotate(label=F('ingredient_tag__label')).values('label', 'unit').annotate(summed_amount=Sum('amount'))

        response = {}
        #serializer = self.get_serializer(ingredients, many=True)
        response['results'] = ingredients
        response['count'] = ingredients.count()

        return Response(response)
