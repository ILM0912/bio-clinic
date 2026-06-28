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
            'created_at',
        )
        read_only_fields = (
            'id',
            'created_at',
        )

    def validate(self, attrs):
        request = self.context['request']
        appointment = Appointment(
            patient=request.user,
            doctor_branch_service=attrs['doctor_branch_service'],
            date_time=attrs['date_time'],
        )
        try:
            appointment.clean()
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages)
        return attrs

    def create(self, validated_data):
        request = self.context['request']
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
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Appointment
        fields = (
            'id',
            'patient_full_name',
            'doctor_full_name',
            'branch_name',
            'service_title',
            'date_time',
            'is_completed',
        )

    def get_patient_full_name(self, obj):
        return obj.patient.get_full_name()

    def get_doctor_full_name(self, obj):
        return obj.doctor_branch_service.doctor.user.get_full_name()


class AppointmentCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('is_completed',)
