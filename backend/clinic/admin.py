from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Appointment,
    Branch,
    BranchService,
    DoctorBranchService,
    DoctorProfile,
    Service,
    ServiceGroup,
    User,
)


class BranchInlineForService(admin.TabularInline):
    model = BranchService
    extra = 1
    autocomplete_fields = ('branch',)


class ServiceInlineForBranch(admin.TabularInline):
    model = BranchService
    extra = 1
    autocomplete_fields = ('service',)


class DoctorInlineForBranchService(admin.TabularInline):
    model = DoctorBranchService
    extra = 1
    autocomplete_fields = ('doctor',)


class BranchServiceInlineForDoctor(admin.TabularInline):
    model = DoctorBranchService
    extra = 1
    autocomplete_fields = ('branch_service',)


class ServiceInlineForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
            }),
        }


class ServiceInlineForServiceGroup(admin.TabularInline):
    model = Service
    form = ServiceInlineForm
    extra = 1


@admin.register(User)
class BioClinicUserAdmin(UserAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
        'is_active',
    )
    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
    )
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name')}),
        ('Роль', {'fields': ('role',)}),
        ('Права доступа', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Служебная информация', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'role',
                'password1',
                'password2',
            ),
        }),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'phone',
    )
    search_fields = (
        'name',
        'address',
        'phone',
    )
    inlines = (ServiceInlineForBranch,)


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    search_fields = ('name',)
    inlines = (ServiceInlineForServiceGroup,)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'group',
        'price',
        'is_active',
    )
    list_editable = ('is_active',)
    list_filter = (
        'group',
        'is_active',
    )
    search_fields = (
        'title',
        'description',
    )
    inlines = (BranchInlineForService,)


@admin.register(BranchService)
class BranchServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'branch',
        'service',
        'is_active',
    )
    list_editable = ('is_active',)
    list_filter = (
        'branch',
        'service',
        'is_active',
    )
    search_fields = (
        'branch__name',
        'service__title',
    )
    inlines = (DoctorInlineForBranchService,)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'specialization',
        'experience_years',
        'is_active',
    )
    list_editable = ('is_active',)
    list_filter = (
        'specialization',
        'is_active',
    )
    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'specialization',
    )
    readonly_fields = ('experience_years',)
    inlines = (BranchServiceInlineForDoctor,)


@admin.register(DoctorBranchService)
class DoctorBranchServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'doctor',
        'branch_service',
        'is_active',
    )
    list_editable = ('is_active',)
    list_filter = (
        'doctor',
        'branch_service',
        'is_active',
    )
    search_fields = (
        'doctor__user__email',
        'doctor__user__first_name',
        'doctor__user__last_name',
        'branch_service__branch__name',
        'branch_service__service__title',
    )

    def has_module_permission(self, request):
        return False


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient',
        'doctor_branch_service',
        'date_time',
        'is_completed',
        'created_at',
    )
    list_filter = (
        'is_completed',
        'doctor_branch_service',
        'date_time',
    )
    search_fields = (
        'patient__email',
        'patient__first_name',
        'patient__last_name',
        'doctor_branch_service__doctor__user__first_name',
        'doctor_branch_service__doctor__user__last_name',
        'doctor_branch_service__branch_service__service__title',
        'doctor_branch_service__branch_service__branch__name',
    )
    date_hierarchy = 'date_time'