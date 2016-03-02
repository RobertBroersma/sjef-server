from usersettings.models import Profile
from rest_framework import viewsets, permissions
from usersettings.serializers import ProfileSerializer
from dry_rest_permissions.generics import DRYPermissions, DRYPermissionFiltersBase
from django.db.models import Q

class ProfileFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        return queryset.filter(Q(user=request.user))


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by()
    serializer_class = ProfileSerializer
    permission_classes = (DRYPermissions,)
    filter_backends = (ProfileFilterBackend,)
