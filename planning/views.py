from planning.models import DayPlanning, MealSetting
from rest_framework import viewsets, permissions
from planning.serializers import DayPlanningSerializer, MealSettingSerializer
from dry_rest_permissions.generics import DRYPermissions, DRYPermissionFiltersBase
from django.db.models import Q

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
