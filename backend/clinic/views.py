from datetime import datetime

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Appointment,
    Branch,
    DoctorBranchService,
    DoctorProfile,
    Service,
    ServiceGroup,
)
from .serializers import (
    AppointmentCreateSerializer,
    BranchSerializer,
    DoctorProfileSerializer,
    DoctorBranchServiceSerializer,
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


class DoctorBranchServiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoctorBranchServiceSerializer

    def get_queryset(self):
        queryset = (
            DoctorBranchService.objects
            .filter(
                is_active=True,
                doctor__is_active=True,
                branch_service__is_active=True,
                branch_service__service__is_active=True,
            )
            .select_related(
                'doctor__user',
                'branch_service__branch',
                'branch_service__service',
            )
            .order_by(
                'branch_service__branch__name',
                'doctor__user__last_name',
                'doctor__user__first_name',
            )
        )
        service_id = self.request.query_params.get('service')
        if service_id:
            queryset = queryset.filter(
                branch_service__service_id=service_id,
            )
        return queryset


class AppointmentViewSet(viewsets.GenericViewSet):
    serializer_class = AppointmentCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return (
            Appointment.objects
            .filter(patient=self.request.user)
            .select_related(
                'patient',
                'doctor_branch_service__doctor__user',
                'doctor_branch_service__branch_service__branch',
                'doctor_branch_service__branch_service__service',
            )
            .order_by('-date_time')
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()

        response_serializer = self.get_serializer(appointment)

        return Response(response_serializer.data, status=201)


    @action(
        detail=False,
        methods=('get',),
        url_path='busy-slots',
        permission_classes=(permissions.AllowAny,),
    )
    def busy_slots(self, request):
        doctor_branch_service_id = request.query_params.get(
            'doctor_branch_service'
        )
        date_value = request.query_params.get('date')

        if not doctor_branch_service_id or not date_value:
            return Response(
                {'detail': 'Необходимо указать врача и дату.'},
                status=400,
            )

        try:
            selected_date = datetime.strptime(
                date_value,
                '%Y-%m-%d',
            ).date()
        except ValueError:
            return Response(
                {'detail': 'Неверный формат даты.'},
                status=400,
            )

        appointments = Appointment.objects.filter(
            doctor_branch_service_id=doctor_branch_service_id,
            date_time__date=selected_date,
        ).exclude(
            status=Appointment.STATUS_CANCELLED,
        )

        busy_slots = [
            appointment.date_time.strftime('%H:%M')
            for appointment in appointments
        ]

        return Response({'busy_slots': busy_slots})