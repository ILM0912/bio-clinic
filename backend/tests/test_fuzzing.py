import pytest
from hypothesis import HealthCheck, given, settings, strategies as st

from clinic.models import Appointment


pytestmark = pytest.mark.django_db


def build_query_params(**params):
    return {
        key: value
        for key, value in params.items()
        if value is not None
    }


@given(
    doctor_branch_service=st.one_of(
        st.none(),
        st.text(),
        st.integers(min_value=-100000, max_value=100000),
    ),
    date_time=st.one_of(
        st.none(),
        st.text(),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
    ),
)
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_create_appointment_fuzzing_does_not_return_500(
    api_client,
    patient,
    doctor_branch_service,
    date_time,
):
    api_client.force_authenticate(user=patient)
    response = api_client.post(
        '/api/appointments/',
        {
            'doctor_branch_service': doctor_branch_service,
            'date_time': date_time,
        },
        format='json',
    )
    assert response.status_code < 500


@given(
    status=st.one_of(
        st.none(),
        st.text(),
        st.integers(),
        st.booleans(),
    )
)
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_update_appointment_status_fuzzing_does_not_return_500(
    api_client,
    patient,
    appointment,
    status,
):
    api_client.force_authenticate(user=patient)
    response = api_client.patch(
        f'/api/appointments/{appointment.id}/',
        {'status': status},
        format='json',
    )
    assert response.status_code < 500


@given(
    date_value=st.text()
)
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_busy_slots_fuzzing_does_not_return_500(
    api_client,
    doctor_branch_service,
    date_value,
):
    response = api_client.get(
        '/api/appointments/busy-slots/',
        {
            'doctor_branch_service': doctor_branch_service.id,
            'date': date_value,
        },
    )
    assert response.status_code < 500


@given(date_value=st.text())
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_doctor_schedule_date_fuzzing_does_not_return_500(
    api_client,
    doctor_user,
    doctor_profile,
    date_value,
):
    api_client.force_authenticate(user=doctor_user)
    response = api_client.get(
        '/api/appointments/',
        {'date': date_value},
    )
    assert response.status_code < 500


@given(
    branch=st.one_of(st.none(), st.text(), st.integers()),
    group=st.one_of(st.none(), st.text(), st.integers()),
)
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_services_filters_fuzzing_does_not_return_500(
    api_client,
    branch,
    group,
):
    response = api_client.get(
        '/api/services/',
        build_query_params(
            branch=branch,
            group=group,
        ),
    )
    assert response.status_code < 500


@given(service=st.one_of(st.none(), st.text(), st.integers()))
@settings(
    max_examples=30,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_doctor_services_filter_fuzzing_does_not_return_500(
    api_client,
    service,
):
    response = api_client.get(
        '/api/doctor-services/',
        build_query_params(service=service),
    )
    assert response.status_code < 500
