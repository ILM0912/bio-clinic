from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

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
    photo = serializers.ImageField(read_only=True)

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
        return Appointment.objects.create(
            patient=request.user,
            **validated_data,
        )