from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from django.db.models import Q
from dry_rest_permissions.generics import DRYPermissionFiltersBase
from core.serializers import UserSerializer, TagSerializer
from core.models import Tag

class IsOwnerFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        return queryset.filter(Q(owner=request.user.profile))

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
