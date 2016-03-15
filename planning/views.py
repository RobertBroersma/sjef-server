from planning.models import DayPlanning, MealSetting, Meal
from rest_framework import viewsets, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.decorators import list_route
from rest_framework.response import Response
from planning.serializers import DayPlanningSerializer, MealSettingSerializer, MealSerializer
from dry_rest_permissions.generics import DRYPermissions, DRYPermissionFiltersBase
from django.db.models import Q
import datetime
import django_filters

class IsOwnerFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        return queryset.filter(Q(owner=request.user.profile))

class DayPlanningViewSet(viewsets.ModelViewSet):
    queryset = DayPlanning.objects.all().order_by()
    serializer_class = DayPlanningSerializer
    permission_classes = (DRYPermissions,)
    filter_backends = (IsOwnerFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)


class MealSettingViewSet(viewsets.ModelViewSet):
    queryset = MealSetting.objects.all().order_by()
    serializer_class = MealSettingSerializer
    permission_classes = (DRYPermissions,)
    filter_backends = (IsOwnerFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)


class MealFilter(filters.FilterSet):
    start_date = django_filters.DateFilter(name="date", lookup_type='gte')
    end_date = django_filters.DateFilter(name="date", lookup_type='lte')
    class Meta:
        model = Meal
        fields = ['start_date', 'end_date']


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (DRYPermissions,)
    filter_backends = (IsOwnerFilterBackend, filters.DjangoFilterBackend)
    filter_class = MealFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)

    @list_route(methods=['post'])
    def generate_mealplan(self, request):
        if 'start' not in request.data:
            return Response('date_start_undefined', status.HTTP_400_BAD_REQUEST)

        if 'end' not in request.data:
            return Response('date_end_undefined', status.HTTP_400_BAD_REQUEST)

        energy = request.user.profile.dri_set.get(nutritional_value__label='calories').amount
        #TODO: Fetch relevant macros from database instead of hardcoding
        macros = {
            'protein': request.user.profile.dri_set.get(nutritional_value__label='protein').amount,
            'fat': request.user.profile.dri_set.get(nutritional_value__label='fat').amount,
            'carbs': request.user.profile.dri_set.get(nutritional_value__label='carbs').amount,
        }
        daterange = {
            'start': datetime.datetime.strptime(request.data['start'], '%Y-%m-%d').date(),
            'end': datetime.datetime.strptime(request.data['end'], '%Y-%m-%d').date()
        }

        mealplan = Meal.generate_mealplan(request.user.profile, energy, macros, daterange)

        serializer = self.get_serializer(mealplan, many=True)
        return Response(serializer.data)
