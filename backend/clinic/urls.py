from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    BranchViewSet,
    DoctorProfileViewSet,
    DoctorBranchServiceViewSet,
    ServiceGroupViewSet,
    ServiceViewSet,
)

router = DefaultRouter()
router.register('branches', BranchViewSet, basename='branches')
router.register('groups', ServiceGroupViewSet, basename='groups')
router.register('services', ServiceViewSet, basename='services')
router.register('doctors', DoctorProfileViewSet, basename='doctors')
router.register(
    'doctor-services',
    DoctorBranchServiceViewSet,
    basename='doctor-services',
)
router.register(
    'appointments',
    AppointmentViewSet,
    basename='appointments',
)

urlpatterns = [
    path('', include(router.urls)),
]
