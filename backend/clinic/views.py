from datetime import datetime, time, timedelta

from django.utils import timezone
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
            .order_by('work_started_at', 'user__last_name', 'user__first_name')
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

        all_slots = []
        current_time = datetime.combine(
            selected_date,
            time(hour=9, minute=0),
        )
        end_time = datetime.combine(
            selected_date,
            time(hour=17, minute=0),
        )

        while current_time < end_time:
            all_slots.append(current_time.strftime('%H:%M'))
            current_time += timedelta(minutes=30)

        now = timezone.localtime()
        if selected_date < now.date():
            return Response({'busy_slots': all_slots})
        if selected_date.weekday() in (5, 6):
            return Response({'busy_slots': all_slots})

        try:
            doctor_branch_service = DoctorBranchService.objects.get(
                id=doctor_branch_service_id
            )
        except DoctorBranchService.DoesNotExist:
            return Response(
                {'detail': 'Связь врача с услугой не найдена.'},
                status=404,
            )

        current_timezone = timezone.get_current_timezone()
        day_start = timezone.make_aware(
            datetime.combine(selected_date, time.min),
            current_timezone,
        )
        day_end = timezone.make_aware(
            datetime.combine(selected_date, time.max),
            current_timezone,
        )

        appointments = Appointment.objects.filter(
            doctor_branch_service__doctor=doctor_branch_service.doctor,
            date_time__gte=day_start,
            date_time__lte=day_end,
        ).exclude(
            status=Appointment.STATUS_CANCELLED,
        )

        busy_slots = [
            timezone.localtime(appointment.date_time).strftime('%H:%M')
            for appointment in appointments
        ]

        if selected_date == now.date():
            for slot in all_slots:
                slot_time = datetime.strptime(slot, '%H:%M').time()

                if slot_time <= now.time():
                    busy_slots.append(slot)

        busy_slots = sorted(set(busy_slots))

        return Response({'busy_slots': busy_slots})
