from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
    )

    ROLE_PATIENT = 'patient'
    ROLE_DOCTOR = 'doctor'
    ROLE_CHOICES = [
        (ROLE_PATIENT, 'Пациент'),
        (ROLE_DOCTOR, 'Врач'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_PATIENT,
        verbose_name='Роль',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name() or self.email 


class Branch(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название филиала',
    )
    address = models.CharField(
        max_length=500,
        verbose_name='Адрес',
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Телефон',
    )

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.name


class ServiceGroup(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название группы',
    )

    class Meta:
        verbose_name = 'Группа услуг'
        verbose_name_plural = 'Группы услуг'

    def __str__(self):
        return self.name


class Service(models.Model):
    group = models.ForeignKey(
        ServiceGroup,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Группа услуг',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название услуги',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Стоимость',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна в клинике',
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title


class BranchService(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='branch_services',
        verbose_name='Филиал',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='branch_services',
        verbose_name='Услуга',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна в филиале',
    )

    class Meta:
        verbose_name = 'Услуга филиала'
        verbose_name_plural = 'Услуги филиалов'
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'service'],
                name='unique_branch_service',
            )
        ]

    def __str__(self):
        return f'{self.branch} - {self.service}'


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name='Пользователь',
    )
    photo = models.ImageField(
        upload_to='doctors/photos/',
        blank=True,
        null=True,
        verbose_name='Фото врача',
    )
    specialization = models.CharField(
        max_length=255,
        verbose_name='Специализация',
    )
    work_started_at = models.DateField(
        verbose_name='Дата начала врачебной практики',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
    )

    @property
    def experience_years(self):
        today = timezone.now().date()
        years = today.year - self.work_started_at.year

        if (today.month, today.day) < (
            self.work_started_at.month,
            self.work_started_at.day,
        ):
            years -= 1

        return years
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.photo:
            from .services import set_doctor_photo

            set_doctor_photo(self)

    class Meta:
        verbose_name = 'Профиль врача'
        verbose_name_plural = 'Профили врачей'

    def __str__(self):
        return f'{self.user} - {self.specialization}'


class DoctorBranchService(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name='doctor_branch_services',
        verbose_name='Врач',
    )
    branch_service = models.ForeignKey(
        BranchService,
        on_delete=models.PROTECT,
        related_name='doctor_branch_services',
        verbose_name='Услуга филиала',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна у врача',
    )

    class Meta:
        verbose_name = 'Услуга врача в филиале'
        verbose_name_plural = 'Услуги врачей в филиалах'
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'branch_service'],
                name='unique_doctor_branch_service',
            )
        ]

    def __str__(self):
        return f'{self.doctor} - {self.branch_service}'


class Appointment(models.Model):
    STATUS_CREATED = 'created'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_CONFIRMED, 'Подтверждена'),
        (STATUS_CANCELLED, 'Отменена'),
        (STATUS_COMPLETED, 'Завершена'),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Пациент',
    )
    doctor_branch_service = models.ForeignKey(
        DoctorBranchService,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='Услуга врача в филиале',
    )
    date_time = models.DateTimeField(
        verbose_name='Дата и время записи',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    def clean(self):
        if not self.doctor_branch_service:
            return

        doctor_branch_service = self.doctor_branch_service
        branch_service = doctor_branch_service.branch_service
        service = branch_service.service
        doctor = doctor_branch_service.doctor

        if not service.is_active:
            raise ValidationError('Услуга отключена в клинике.')

        if not branch_service.is_active:
            raise ValidationError('Услуга недоступна в выбранном филиале.')

        if not doctor.is_active:
            raise ValidationError('Врач неактивен.')

        if not doctor_branch_service.is_active:
            raise ValidationError(
                'Врач не оказывает эту услугу в выбранном филиале.'
            )

        if self.date_time and self.date_time <= timezone.now():
            raise ValidationError('Нельзя записаться на прошедшее время.')
        
        if Appointment.objects.filter(
            doctor_branch_service=doctor_branch_service,
            date_time=self.date_time,
        ).exclude(pk=self.pk).exclude(
            status=self.STATUS_CANCELLED,
        ).exists():
            raise ValidationError('На выбранное время врач уже занят.')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date_time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor_branch_service', 'date_time'],
                name='unique_doctor_appointment_time',
            )
        ]

    def __str__(self):
        return (
            f'{self.patient} - '
            f'{self.doctor_branch_service.branch_service.service} - '
            f'{self.date_time}'
        )
