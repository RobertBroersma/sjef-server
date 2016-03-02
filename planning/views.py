from planning.models import DayPlanning
from rest_framework import viewsets, permissions
from planning.serializers import DayPlanningSerializer
from dry_rest_permissions.generics import DRYPermissions


class DayPlanningViewSet(viewsets.ModelViewSet):
    queryset = DayPlanning.objects.all().order_by()
    serializer_class = DayPlanningSerializer
    permission_classes = (DRYPermissions,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)
