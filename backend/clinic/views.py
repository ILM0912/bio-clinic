from rest_framework import viewsets

from .models import Branch, DoctorProfile, Service, ServiceGroup
from .serializers import (
    BranchSerializer,
    DoctorProfileSerializer,
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


class DoctorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoctorProfileSerializer
    def get_queryset(self):
        return (
            DoctorProfile.objects
            .filter(is_active=True)
            .select_related('user')
            .order_by('user__last_name', 'user__first_name')
        )
