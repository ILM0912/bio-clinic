from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BranchViewSet,
    DoctorProfileViewSet,
    ServiceGroupViewSet,
    ServiceViewSet,
)

router = DefaultRouter()
router.register('branches', BranchViewSet, basename='branches')
router.register('groups', ServiceGroupViewSet, basename='groups')
router.register('services', ServiceViewSet, basename='services')
router.register('doctors', DoctorProfileViewSet, basename='doctors')

urlpatterns = [
    path('', include(router.urls)),
]
