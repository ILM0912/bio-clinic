from rest_framework import permissions


class IsAppointmentOwnerOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if view.action in ('list', 'retrieve', 'create', 'busy_slots'):
            return True
        if view.action in ('partial_update', 'update'):
            return request.user.role in (
                request.user.ROLE_PATIENT,
                request.user.ROLE_DOCTOR,
            )
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action == 'retrieve':
            if user.role == user.ROLE_PATIENT:
                return obj.patient == user
            if user.role == user.ROLE_DOCTOR:
                return obj.doctor_branch_service.doctor == user.doctor_profile
            return False

        if view.action in ('partial_update', 'update'):
            if user.role == user.ROLE_PATIENT:
                return obj.patient == user
            if user.role == user.ROLE_DOCTOR:
                return obj.doctor_branch_service.doctor == user.doctor_profile
            return False
        return True
