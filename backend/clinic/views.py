from rest_framework import viewsets

from .models import Branch, Service, ServiceGroup
from .serializers import (
    BranchSerializer,
    ServiceGroupSerializer,
    ServiceSerializer,
)


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class ServiceGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceGroup.objects.all()
    serializer_class = ServiceGroupSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceSerializer
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)
        branch_id = self.request.query_params.get('branch')
        group_id = self.request.query_params.get('group')
        if branch_id:
            queryset = queryset.filter(
                branch_services__branch_id=branch_id,
                branch_services__is_active=True,
            )
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        return queryset.distinct()
