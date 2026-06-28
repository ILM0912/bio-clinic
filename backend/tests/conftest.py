from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from clinic.models import (
    Appointment,
    Branch,
    BranchService,
    DoctorBranchService,
    DoctorProfile,
    Service,
    ServiceGroup,
    User,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def patient():
    return User.objects.create_user(
        email='patient@test.ru',
        password='testpassword',
        first_name='Иван',
        last_name='Иванов',
        role=User.ROLE_PATIENT,
    )


@pytest.fixture
def another_patient():
    return User.objects.create_user(
        email='another@test.ru',
        password='testpassword',
        first_name='Петр',
        last_name='Петров',
        role=User.ROLE_PATIENT,
    )


@pytest.fixture
def doctor_user():
    return User.objects.create_user(
        email='doctor@test.ru',
        password='testpassword',
        first_name='Анна',
        last_name='Смирнова',
        role=User.ROLE_DOCTOR,
    )


@pytest.fixture
def doctor_profile(doctor_user):
    return DoctorProfile.objects.create(
        user=doctor_user,
        specialization='Терапевт',
        work_started_at='2020-01-01',
        is_active=True,
    )


@pytest.fixture
def another_doctor_user():
    return User.objects.create_user(
        email='another_doctor@test.ru',
        password='testpassword',
        first_name='Мария',
        last_name='Кузнецова',
        role=User.ROLE_DOCTOR,
    )


@pytest.fixture
def another_doctor_profile(another_doctor_user):
    return DoctorProfile.objects.create(
        user=another_doctor_user,
        specialization='Кардиолог',
        work_started_at='2021-01-01',
        is_active=True,
    )


@pytest.fixture
def branch():
    return Branch.objects.create(
        name='BioClinic Центральная',
        address='Москва, ул. Примерная, д. 10',
        phone='+79990000000',
    )


@pytest.fixture
def service_group():
    return ServiceGroup.objects.create(name='Терапия')


@pytest.fixture
def service(service_group):
    return Service.objects.create(
        group=service_group,
        title='Консультация терапевта',
        description='Первичный приём терапевта',
        price=1500,
        is_active=True,
    )


@pytest.fixture
def branch_service(branch, service):
    return BranchService.objects.create(
        branch=branch,
        service=service,
        is_active=True,
    )


@pytest.fixture
def doctor_branch_service(doctor_profile, branch_service):
    return DoctorBranchService.objects.create(
        doctor=doctor_profile,
        branch_service=branch_service,
        is_active=True,
    )


@pytest.fixture
def future_datetime():
    now = timezone.localtime()
    future = now + timedelta(days=3)

    while future.weekday() in (5, 6):
        future += timedelta(days=1)

    return future.replace(hour=10, minute=0, second=0, microsecond=0)


@pytest.fixture
def past_datetime():
    past = timezone.localtime() - timedelta(days=3)

    while past.weekday() in (5, 6):
        past -= timedelta(days=1)

    return past.replace(hour=10, minute=0, second=0, microsecond=0)


@pytest.fixture
def appointment(patient, doctor_branch_service, future_datetime):
    return Appointment.objects.create(
        patient=patient,
        doctor_branch_service=doctor_branch_service,
        date_time=future_datetime,
        is_completed=False,
    )
