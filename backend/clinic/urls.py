from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BranchViewSet, ServiceGroupViewSet, ServiceViewSet

router = DefaultRouter()
router.register('branches', BranchViewSet, basename='branches')
router.register('groups', ServiceGroupViewSet, basename='groups')
router.register('services', ServiceViewSet, basename='services')

urlpatterns = [
    path('', include(router.urls)),
]
