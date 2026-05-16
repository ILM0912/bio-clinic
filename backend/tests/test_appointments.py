import pytest
from django.urls import reverse

from clinic.models import Appointment


pytestmark = pytest.mark.django_db


def test_patient_can_create_appointment(
    api_client,
    patient,
    doctor_branch_service,
    future_datetime,
):
    api_client.force_authenticate(user=patient)

    response = api_client.post(
        '/api/appointments/',
        {
            'doctor_branch_service': doctor_branch_service.id,
            'date_time': future_datetime.isoformat(),
        },
        format='json',
    )

    assert response.status_code == 201
    assert Appointment.objects.count() == 1
    assert Appointment.objects.first().patient == patient


def test_anonymous_user_cannot_create_appointment(
    api_client,
    doctor_branch_service,
    future_datetime,
):
    response = api_client.post(
        '/api/appointments/',
        {
            'doctor_branch_service': doctor_branch_service.id,
            'date_time': future_datetime.isoformat(),
        },
        format='json',
    )

    assert response.status_code == 401


def test_patient_can_see_upcoming_appointments(
    api_client,
    patient,
    appointment,
):
    api_client.force_authenticate(user=patient)

    response = api_client.get('/api/appointments/?scope=upcoming')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == appointment.id


def test_patient_cannot_see_another_patient_appointment(
    api_client,
    another_patient,
    appointment,
):
    api_client.force_authenticate(user=another_patient)

    response = api_client.get('/api/appointments/')

    assert response.status_code == 200
    assert len(response.data) == 0


def test_patient_can_cancel_own_future_appointment(
    api_client,
    patient,
    appointment,
):
    api_client.force_authenticate(user=patient)

    response = api_client.patch(
        f'/api/appointments/{appointment.id}/',
        {'status': Appointment.STATUS_CANCELLED},
        format='json',
    )

    appointment.refresh_from_db()

    assert response.status_code == 200
    assert appointment.status == Appointment.STATUS_CANCELLED


def test_patient_cannot_complete_appointment(
    api_client,
    patient,
    appointment,
):
    api_client.force_authenticate(user=patient)

    response = api_client.patch(
        f'/api/appointments/{appointment.id}/',
        {'status': Appointment.STATUS_COMPLETED},
        format='json',
    )

    appointment.refresh_from_db()

    assert response.status_code == 400
    assert appointment.status == Appointment.STATUS_CREATED


def test_doctor_can_see_own_schedule(
    api_client,
    doctor_user,
    appointment,
    future_datetime,
):
    api_client.force_authenticate(user=doctor_user)

    response = api_client.get(
        f'/api/appointments/?date={future_datetime.date()}'
    )

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == appointment.id


def test_doctor_can_complete_appointment(
    api_client,
    doctor_user,
    appointment,
):
    api_client.force_authenticate(user=doctor_user)

    response = api_client.patch(
        f'/api/appointments/{appointment.id}/',
        {'status': Appointment.STATUS_COMPLETED},
        format='json',
    )

    appointment.refresh_from_db()

    assert response.status_code == 200
    assert appointment.status == Appointment.STATUS_COMPLETED


def test_doctor_cannot_cancel_appointment(
    api_client,
    doctor_user,
    appointment,
):
    api_client.force_authenticate(user=doctor_user)

    response = api_client.patch(
        f'/api/appointments/{appointment.id}/',
        {'status': Appointment.STATUS_CANCELLED},
        format='json',
    )

    appointment.refresh_from_db()

    assert response.status_code == 400
    assert appointment.status == Appointment.STATUS_CREATED


def test_doctor_schedule_returns_400_for_invalid_date(
    api_client,
    doctor_user,
    doctor_profile,
):
    api_client.force_authenticate(user=doctor_user)
    response = api_client.get('/api/appointments/?date=test')
    assert response.status_code == 400


def test_doctor_cannot_see_another_doctor_schedule(
    api_client,
    another_doctor_user,
    another_doctor_profile,
    appointment,
    future_datetime,
):
    api_client.force_authenticate(user=another_doctor_user)
    response = api_client.get(
        f'/api/appointments/?date={future_datetime.date()}'
    )
    assert response.status_code == 200
    assert len(response.data) == 0