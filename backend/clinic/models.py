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
        today = timezone.localtime(timezone.now()).date()

        if self.work_started_at >= today:
            return 0

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
    is_completed = models.BooleanField(
        default=False,
        verbose_name='Завершена',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    def clean(self):
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

        appointment_time = self.date_time

        if timezone.is_naive(appointment_time):
            appointment_time = timezone.make_aware(
                appointment_time,
                timezone.get_current_timezone(),
            )

        local_appointment_time = timezone.localtime(appointment_time)
        local_now = timezone.localtime()
        if local_appointment_time <= local_now:
            raise ValidationError('Нельзя записаться на прошедшее время.')
        if local_appointment_time.weekday() in (5, 6):
            raise ValidationError('Запись доступна только в будние дни.')
        if local_appointment_time.hour < 9 or local_appointment_time.hour >= 17:
            raise ValidationError('Запись доступна только с 09:00 до 17:00.')
        if local_appointment_time.minute not in (0, 30):
            raise ValidationError('Запись доступна только с шагом 30 минут.')

        if Appointment.objects.filter(
            doctor_branch_service__doctor=doctor,
            date_time=self.date_time,
        ).exclude(pk=self.pk).exists():
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
