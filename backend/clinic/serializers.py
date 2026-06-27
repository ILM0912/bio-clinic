from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

from .models import (
    Appointment,
    Branch,
    DoctorBranchService,
    DoctorProfile,
    Service,
    ServiceGroup,
    User,
)


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = (
            'id',
            'name',
            'address',
            'phone',
        )


class ServiceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGroup
        fields = (
            'id',
            'name',
        )


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id',
            'group',
            'title',
            'description',
            'price',
        )


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
        )


class DoctorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name',
        read_only=True,
    )
    last_name = serializers.CharField(
        source='user.last_name',
        read_only=True,
    )
    experience_years = serializers.IntegerField(read_only=True)
    photo = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
            'specialization',
            'experience_years',
        )

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None


class DoctorBranchServiceSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(read_only=True)
    branch = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    class Meta:
        model = DoctorBranchService
        fields = (
            'id',
            'doctor',
            'branch',
            'service',
        )

    def get_branch(self, obj):
        return BranchSerializer(obj.branch_service.branch).data

    def get_service(self, obj):
        return ServiceSerializer(obj.branch_service.service).data


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'id',
            'doctor_branch_service',
            'date_time',
            'status',
            'created_at',
        )
        read_only_fields = (
            'id',
            'status',
            'created_at',
        )

    def validate(self, attrs):
        request = self.context.get('request')
        appointment = Appointment(
            patient=request.user,
            doctor_branch_service=attrs.get('doctor_branch_service'),
            date_time=attrs.get('date_time'),
        )
        try:
            appointment.clean()
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages)
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        try:
            return Appointment.objects.create(
                patient=request.user,
                **validated_data,
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'На выбранное время врач уже занят.'
            )


class AppointmentReadSerializer(serializers.ModelSerializer):
    patient_full_name = serializers.SerializerMethodField()
    doctor_full_name = serializers.SerializerMethodField()
    branch_name = serializers.CharField(
        source='doctor_branch_service.branch_service.branch.name',
        read_only=True,
    )
    service_title = serializers.CharField(
        source='doctor_branch_service.branch_service.service.title',
        read_only=True,
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True,
    )

    class Meta:
        model = Appointment
        fields = (
            'id',
            'patient_full_name',
            'doctor_full_name',
            'branch_name',
            'service_title',
            'date_time',
            'status',
            'status_display',
        )

    def get_patient_full_name(self, obj):
        return obj.patient.get_full_name()

    def get_doctor_full_name(self, obj):
        return obj.doctor_branch_service.doctor.user.get_full_name()


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('status',)

    def validate_status(self, value):
        request = self.context['request']
        user = request.user
        if user.role == user.ROLE_PATIENT:
            if value != Appointment.STATUS_CANCELLED:
                raise serializers.ValidationError(
                    'Пациент может только отменить запись.'
                )
        elif user.role == user.ROLE_DOCTOR:
            if value != Appointment.STATUS_COMPLETED:
                raise serializers.ValidationError(
                    'Врач может только завершить запись.'
                )
        else:
            raise serializers.ValidationError(
                'Недопустимое изменение статуса.'
            )
        return value

    def validate(self, attrs):
        appointment = self.instance
        user = self.context['request'].user
        if user.role == user.ROLE_PATIENT:
            if appointment.date_time < timezone.now():
                raise serializers.ValidationError(
                    'Нельзя отменить прошедшую запись.'
                )
            if appointment.status != Appointment.STATUS_CREATED:
                raise serializers.ValidationError(
                    'Можно отменить только активную запись.'
                )
        if user.role == user.ROLE_DOCTOR:
            if appointment.status == Appointment.STATUS_CANCELLED:
                raise serializers.ValidationError(
                    'Нельзя завершить отменённую запись.'
                )
        return attrs
